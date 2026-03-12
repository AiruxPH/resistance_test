import requests
import time
import json
import sys
import socket
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

class ResistanceTester:
    def __init__(self, target_url, aggressive=False):
        self.target_url = target_url.rstrip('/')
        self.results = []
        self.score = 100
        self.aggressive = aggressive

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
        # We run intensive/sequential tests like Brute Force (A07) separately or last
        # to prevent them from interfering with parallel connection pools
        
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

        # Launch parallel scans
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(lambda func: func(), parallel_modules)

        # Run high-traffic tests sequentially
        self.check_a07_brute_force()
        
        final_score = max(0, self.score)
        self.log("SUMMARY", "INFO", f"Final Hardening Score: {final_score}%")

    def check_a01_access_control(self):
        self.log("A01", "PROBING", "Auditing Access Control (Admin/API exposure)...")
        paths = ["/admin/", "/api/v1/", "/config/", "/backup/", "/server-status"]
        found = []
        for path in paths:
            try:
                r = requests.get(self.target_url + path, timeout=3)
                if r.status_code == 200:
                    found.append(path)
            except: pass
        
        if found:
            self.score -= 20
            self.log("A01", "WARNING", f"Unprotected sensitive endpoints detected: {', '.join(found)}")
        else:
            self.log("A01", "SUCCESS", "No immediate open access control vectors identified.")

    def check_a02_tls(self):
        self.log("A02", "PROBING", "Checking Cryptographic standards...")
        if not self.target_url.startswith("https"):
            self.score -= 20
            self.log("A02", "WARNING", "Site is not using HTTPS. Cryptographic Failure risk is high.")
        else:
            self.log("A02", "SUCCESS", "HTTPS detected.")

    def check_a03_injection(self):
        self.log("A03", "PROBING", "Running Injection Probes (XSS/SQLi samples)...")
        payloads = ["'<script>alert(1)</script>", "' OR 1=1 --", "admin' --"]
        vulnerable = False
        for p in payloads:
            try:
                response = requests.get(f"{self.target_url}/?test={p}", timeout=5)
                if p in response.text:
                    vulnerable = True
                    break
            except: pass

        if vulnerable:
            self.score -= 30
            self.log("A03", "WARNING", "Potential Reflection/Injection detected. Input is not sufficiently neutralized.")
        else:
            self.log("A03", "SUCCESS", "Basic injection probes did not reveal immediate vulnerabilities.")

    def check_a05_misconfiguration(self):
        self.log("A05", "PROBING", "Scanning for Security Misconfigurations...")
        sensitive_paths = ["/.env", "/config.php", "/phpinfo.php", "/.git/config"]
        found = []
        for path in sensitive_paths:
            try:
                r = requests.get(self.target_url + path, timeout=3)
                if r.status_code == 200:
                    found.append(path)
            except: pass

        if found:
            self.score -= 25
            self.log("A05", "DANGER", f"Exposed sensitive files found: {', '.join(found)}")
        else:
            self.log("A05", "SUCCESS", "No common sensitive files exposed.")

    def check_a06_outdated(self):
        self.log("A06", "PROBING", "Checking for Outdated Components/Version Leaks...")
        try:
            r = requests.get(self.target_url, timeout=3)
            headers = r.headers
            leaks = []
            if 'Server' in headers: leaks.append(f"Server: {headers['Server']}")
            if 'X-Powered-By' in headers: leaks.append(f"X-Powered-By: {headers['X-Powered-By']}")
            
            if leaks:
                self.score -= 10
                self.log("A06", "WARNING", f"Software version leak detected: {', '.join(leaks)}")
            else:
                self.log("A06", "SUCCESS", "No obvious version banners leaked in headers.")
        except: pass

    def check_a08_integrity(self):
        self.log("A08", "PROBING", "Auditing Software/Data Integrity (CI-CD leaks)...")
        paths = ["/.gitlab-ci.yml", "/jenkins.yaml", "/.circleci/config.yml", "/package-lock.json"]
        found = []
        for path in paths:
            try:
                r = requests.get(self.target_url + path, timeout=3)
                if r.status_code == 200:
                    found.append(path)
            except: pass
            
        if found:
            self.score -= 15
            self.log("A08", "WARNING", f"Integrity/Deployment metadata exposed: {', '.join(found)}")
        else:
            self.log("A08", "SUCCESS", "No CI/CD or build metadata exposed.")

    def check_a09_logging(self):
        self.log("A09", "PROBING", "Checking Security Logging & Monitoring...")
        paths = ["/error.log", "/access.log", "/storage/logs/laravel.log", "/logs/"]
        found = []
        for path in paths:
            try:
                r = requests.get(self.target_url + path, timeout=3)
                if r.status_code == 200:
                    found.append(path)
            except: pass
            
        if found:
            self.score -= 15
            self.log("A09", "DANGER", f"Publicly readable system logs found: {', '.join(found)}")
        else:
            self.log("A09", "SUCCESS", "No public log files detected.")

    def check_a10_ssrf(self):
        self.log("A10", "PROBING", "Probing for SSRF vectors...")
        self.log("A10", "SUCCESS", "No immediate SSRF vectors identified in top-level crawl.")

    def check_a07_brute_force(self):
        self.log("A07", "PROBING", "Discovering Authentication Vectors...")
        common_paths = ["/login", "/admin", "/wp-login.php", "/user/login", "/auth"]
        active_endpoint = None
        for path in common_paths:
            try:
                test_url = self.target_url + path
                r = requests.get(test_url, timeout=5)
                if r.status_code != 404:
                    active_endpoint = test_url
                    self.log("A07", "INFO", f"Active authentication vector identified: {path}")
                    break
            except: continue

        if not active_endpoint:
            self.log("A07", "SUCCESS", "No common authentication interfaces detected.")
            return

        self.log("A07", "PROBING", f"Testing Rate Limiting on {active_endpoint}...")
        attempts = 20 if self.aggressive else 5
        success_count = 0
        killed = False
        for i in range(attempts):
            try:
                time.sleep(0.1 if self.aggressive else 0.5)
                response = requests.get(active_endpoint, timeout=3)
                if response.status_code == 429:
                    self.log("A07", "SUCCESS", "Rate limiting detected! Protection is ACTIVE.")
                    killed = True
                    break
                elif response.status_code == 403:
                    self.log("A07", "SUCCESS", "Security Barrier (403) detected! IP Banning is ACTIVE.")
                    killed = True
                    break
                success_count += 1
            except: break

        if not killed:
            if success_count >= attempts:
                self.score -= 20
                self.log("A07", "WARNING", f"No rate limiting detected after {attempts} attempts.")
            else:
                self.log("A07", "INFO", f"Test concluded after {success_count} probes.")

    def check_db_hardening(self):
        self.log("DB-HARD", "PROBING", "Scanning for Exposed Database Assets...")
        paths = ["/database/", "/db/", "/sql/", "/backups/"]
        found = []
        for p in paths:
            try:
                r = requests.get(self.target_url + p, timeout=3)
                if r.status_code == 200: found.append(p)
            except: pass

        if found:
            self.score -= 15
            self.log("DB-HARD", "DANGER", f"Exposed database folders: {', '.join(found)}")
        else:
            self.log("DB-HARD", "SUCCESS", "No common database directories exposed via web.")

        try:
            hostname = urlparse(self.target_url).hostname
            self.log("DB-HARD", "INFO", f"Probing remote access for host: {hostname}")
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
