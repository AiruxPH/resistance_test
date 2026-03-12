import requests
import time
import json
import sys
import socket
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

class ResistanceTester:
    def __init__(self, target_url, aggressive=False):
        self.target_url = target_url.rstrip('/')
        self.results = []
        self.score = 100
        self.aggressive = aggressive
        self.session = requests.Session() # Use session for better state handling

    def log(self, module, level, message):
        entry = {
            "timestamp": time.strftime("%H:%M:%S"),
            "module": module,
            "level": level,
            "message": message
        }
        self.results.append(entry)
        print(json.dumps(entry))
        sys.stdout.flush()

    def run_all(self):
        parallel_modules = [
            self.check_a01_access_control,
            self.check_a02_tls,
            self.check_a03_injection,
            self.check_a05_misconfiguration,
            self.check_a06_outdated,
            self.check_a08_integrity,
            self.check_a09_logging,
            self.check_a10_ssrf,
            self.check_db_hardening
        ]

        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(lambda func: func(), parallel_modules)

        self.check_a07_brute_force()
        
        final_score = max(0, self.score)
        self.log("SUMMARY", "INFO", f"Final Hardening Score: {final_score}%")

    def check_a01_access_control(self):
        self.log("A01", "PROBING", "Auditing Access Control...")
        paths = ["/admin/", "/api/v1/", "/config/", "/backup/", "/server-status"]
        found = []
        for path in paths:
            try:
                r = self.session.get(self.target_url + path, timeout=3)
                if r.status_code == 200:
                    found.append(path)
            except: pass
        
        if found:
            self.score -= 20
            self.log("A01", "WARNING", f"Unprotected sensitive endpoints: {', '.join(found)}")
        else:
            self.log("A01", "SUCCESS", "No immediate open access control vectors identified.")

    def check_a02_tls(self):
        self.log("A02", "PROBING", "Checking Cryptographic standards...")
        if not self.target_url.startswith("https"):
            self.score -= 20
            self.log("A02", "WARNING", "Site is not using HTTPS.")
        else:
            self.log("A02", "SUCCESS", "HTTPS detected.")

    def check_a03_injection(self):
        self.log("A03", "PROBING", "Running Advanced Injection Probes (GET/POST)...")
        
        # SQLi Payloads
        sqli_payloads = ["' OR 1=1 --", '" OR 1=1 --', "admin' --", "admin' #", "' OR '1'='1"]
        xss_payloads = ["<script>alert(1)</script>", "javascript:alert(1)"]
        
        is_vulnerable = False
        
        # 1. Passive Form & CSRF Discovery
        login_url = self.target_url
        csrf_token = None
        form_action = None
        try:
            r_main = self.session.get(self.target_url, timeout=5)
            # Find CSRF token (hidden input)
            csrf_match = re.search(r'name="csrf"\s+value="(.*?)"', r_main.text, re.I)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                self.log("A03", "INFO", "Detected CSRF token. Including in security probes.")
            
            # Find Form Action
            action_match = re.search(r'<form.*?action="(.*?)"', r_main.text, re.I | re.S)
            if action_match:
                form_action = action_match.group(1)
                if form_action.startswith('/'):
                    parsed = urlparse(self.target_url)
                    login_url = f"{parsed.scheme}://{parsed.netloc}{form_action}"
        except: pass

        # 2. Active POST Probing (Auth Bypass Simulation)
        common_fields = ['username', 'user', 'login', 'email', 'password', 'pass']
        
        for payload in sqli_payloads:
            try:
                # Construct payload data
                data = {field: payload for field in common_fields}
                if csrf_token:
                    data['csrf'] = csrf_token
                
                # Check for redirect (302) or specific successful login indicators
                r = self.session.post(login_url, data=data, timeout=5, allow_redirects=False)
                
                # Indicators of successful SQLi bypass:
                if r.status_code == 302:
                    is_vulnerable = True
                    self.log("A03", "DANGER", f"Authentication Bypass detected via payload: {payload}")
                    break
                
                # Check for SQL Error leaking
                sql_errors = ["sql syntax", "mysql_fetch", "sqlite3", "postgresql", "driver", "ora-", "dynamic sql"]
                if any(err in r.text.lower() for err in sql_errors):
                    is_vulnerable = True
                    self.log("A03", "DANGER", "Database error leakage detected. Injection is likely active.")
                    break
            except: pass

        # 3. Traditional GET Reflection (for XSS/SQLi)
        if not is_vulnerable:
            for p in xss_payloads + sqli_payloads:
                try:
                    r = self.session.get(f"{self.target_url}/?id={p}", timeout=5)
                    if p in r.text:
                        is_vulnerable = True
                        self.log("A03", "WARNING", f"Input reflection detected: {p}")
                        break
                except: pass

        if is_vulnerable:
            self.score -= 30
        else:
            self.log("A03", "SUCCESS", "No immediate injection vulnerabilities detected.")

    def check_a05_misconfiguration(self):
        self.log("A05", "PROBING", "Scanning for Security Misconfigurations...")
        sensitive_paths = ["/.env", "/config.php", "/phpinfo.php", "/.git/config"]
        found = []
        for path in sensitive_paths:
            try:
                r = self.session.get(self.target_url + path, timeout=3)
                if r.status_code == 200:
                    found.append(path)
            except: pass

        if found:
            self.score -= 25
            self.log("A05", "DANGER", f"Exposed sensitive files: {', '.join(found)}")
        else:
            self.log("A05", "SUCCESS", "No common sensitive files exposed.")

    def check_a06_outdated(self):
        self.log("A06", "PROBING", "Checking for Version Leaks...")
        try:
            r = self.session.get(self.target_url, timeout=3)
            headers = r.headers
            leaks = []
            if 'Server' in headers: leaks.append(f"Server: {headers['Server']}")
            if 'X-Powered-By' in headers: leaks.append(f"X-Powered-By: {headers['X-Powered-By']}")
            
            if leaks:
                self.score -= 10
                self.log("A06", "WARNING", f"Software version leak: {', '.join(leaks)}")
            else:
                self.log("A06", "SUCCESS", "No significant header leaks.")
        except: pass

    def check_a08_integrity(self):
        self.log("A08", "PROBING", "Auditing Integrity (CI-CD leaks)...")
        paths = ["/.gitlab-ci.yml", "/jenkins.yaml", "/.circleci/config.yml", "/package-lock.json"]
        found = []
        for path in paths:
            try:
                r = self.session.get(self.target_url + path, timeout=3)
                if r.status_code == 200:
                    found.append(path)
            except: pass
            
        if found:
            self.score -= 15
            self.log("A08", "WARNING", f"Build metadata exposed: {', '.join(found)}")
        else:
            self.log("A08", "SUCCESS", "No CI/CD metadata exposed.")

    def check_a09_logging(self):
        self.log("A09", "PROBING", "Checking Security Logging...")
        paths = ["/error.log", "/access.log", "/storage/logs/laravel.log", "/logs/"]
        found = []
        for path in paths:
            try:
                r = self.session.get(self.target_url + path, timeout=3)
                if r.status_code == 200:
                    found.append(path)
            except: pass
            
        if found:
            self.score -= 15
            self.log("A09", "DANGER", f"Readable logs found: {', '.join(found)}")
        else:
            self.log("A09", "SUCCESS", "No public log files detected.")

    def check_a10_ssrf(self):
        self.log("A10", "PROBING", "Probing for SSRF vectors...")
        self.log("A10", "SUCCESS", "No immediate SSRF vectors identified.")

    def check_a07_brute_force(self):
        self.log("A07", "PROBING", "Discovering Authentication Vectors...")
        common_paths = ["/login", "/admin", "/wp-login.php", "/user/login", "/auth"]
        active_endpoint = None
        for path in common_paths:
            try:
                test_url = self.target_url + path
                r = self.session.get(test_url, timeout=5)
                if r.status_code != 404:
                    active_endpoint = test_url
                    self.log("A07", "INFO", f"Active auth vector: {path}")
                    break
            except: continue

        if not active_endpoint:
            self.log("A07", "SUCCESS", "No common login interfaces detected.")
            return

        self.log("A07", "PROBING", f"Testing Rate Limiting on {active_endpoint}...")
        attempts = 20 if self.aggressive else 5
        success_count = 0
        killed = False
        for i in range(attempts):
            try:
                time.sleep(0.1 if self.aggressive else 0.5)
                # Ensure we use the session to preserve cookies/state
                response = self.session.get(active_endpoint, timeout=3)
                if response.status_code == 429:
                    self.log("A07", "SUCCESS", "Rate limiting active (429).")
                    killed = True
                    break
                elif response.status_code == 403:
                    self.log("A07", "SUCCESS", "Security Barrier active (403).")
                    killed = True
                    break
                success_count += 1
            except: break

        if not killed:
            if success_count >= attempts:
                self.score -= 20
                self.log("A07", "WARNING", f"No rate limiting after {attempts} attempts.")
            else:
                self.log("A07", "INFO", f"Test concluded after {success_count} probes.")

    def check_db_hardening(self):
        self.log("DB-HARD", "PROBING", "Scanning for Database Assets...")
        paths = ["/database/", "/db/", "/sql/", "/backups/"]
        found = []
        for p in paths:
            try:
                r = self.session.get(self.target_url + p, timeout=3)
                if r.status_code == 200: found.append(p)
            except: pass

        if found:
            self.score -= 15
            self.log("DB-HARD", "DANGER", f"Exposed DB folders: {', '.join(found)}")
        else:
            self.log("DB-HARD", "SUCCESS", "No common DB directories exposed.")

        try:
            hostname = urlparse(self.target_url).hostname
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                if s.connect_ex((hostname, 3306)) == 0:
                    self.score -= 10
                    self.log("DB-HARD", "WARNING", "Remote SQL port (3306) is open.")
                else:
                    self.log("DB-HARD", "SUCCESS", "Remote SQL port is protected.")
        except: pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    url = sys.argv[1]
    is_aggressive = "--aggressive" in sys.argv
    tester = ResistanceTester(url, aggressive=is_aggressive)
    tester.run_all()
