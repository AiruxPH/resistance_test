# 🛡️ Resistance Test - Security Hardening & Vulnerability Dashboard

**Resistance Test** is an automated, high-performance **security hardening analysis tool** and **vulnerability scanner**. It is designed to evaluate web application security against the **OWASP Top 10**, featuring **Honey-Token (Canary) generation**, **Brute Force detection**, and **Database Hardening** audits.

Built on the **Global Prevention Strategy**, this suite provides a "one-click" forensic dashboard for developers, security researchers, and penetration testers to verify system resistance.

---

## ⚠️ LEGAL DISCLAIMER & ETHICAL USE

**FOR AUTHORIZED TESTING ONLY.** This tool is designed to help developers and security researchers verify the "resistance" of their own systems. 
- **NEVER** use this tool against targets you do not own or have explicit written permission to test.
- The authors are not responsible for any misuse or damage caused by this tool. 
- Using this tool against public infrastructure (like Google, etc.) without permission is illegal and may result in IP banning or legal action.

---

## 🚀 Quick Start (Windows)

1. **Download/Clone** this repository.
2. **Double-click `start.bat`.**
   - This script will check for Python. If missing, it will help you install it.
   - It will automatically install all required libraries (`flask`, `requests`, etc.).
   - It will launch the server and open the Dashboard in your browser automatically.

## 🐧 Quick Start (Linux/macOS/Advanced)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the launcher:**
   ```bash
   python run.py
   ```
3. **Open the UI:**
   Navigate to `http://127.0.0.1:5000` in your web browser.

---

## 📂 Project Structure

- `core/`: **The "Brain"** - Contains the testing engine (`tester.py`) and canary generators.
- `ui/`: **The "Face"** - Contains the HTML/CSS/JS for the dashboard.
- `server.py`: The unified backend and web server.
- `run.py`: The Python-based automation launcher.
- `start.bat`: The Windows-friendly bootstrap script.

---

## ⚙️ Security Modules

- **A02 Cryptographic Failure:** Verify HTTPS and TLS enforcement.
- **A03 Injection Probes:** Test for SQL Injection and XSS reflection.
- **A05 Security Misconfiguration:** Scans for exposed `.env`, `config.php`, and `.git` files.
- **A07 Brute Force Resistance:** Test rate-limiting with intelligent kill-switches to prevent IP banning.
- **A10 SSRF Probe:** Analyze server-side request forgery risks.
- **DB Hardening Check:** Verifies database folder visibility (User Rule #5) and remote SQL port security (Rule #8).
- **Forensic Traps (Honey-Tokens):** Generate decoy credentials to detect unauthorized snooping.

---

## 🕵️ Advanced Strategy: Forensic Decoys (Honey-Tokens)

The **Forensic Trap** module doesn't just scan for bugs—it sets an active "Digital Tripwire" for hackers.

### 1. The Strategy
A Decoy file is a piece of "Bait" that looks like a sensitive credential but is actually fake. Normal users will never look for these files, but a hacker using automated tools or manual snooping will find them immediately.

### 2. How to Deploy
1. **Generate:** Use the buttons on the dashboard to generate `.env`, `SQL Config`, or `Root Keys`.
2. **Setup:** Create a file with the corresponding name (e.g., `.env`) in your server's root directory.
3. **Bait:** Paste the generated fake content into that file.

### 3. Catching the Attacker
If anyone accesses these files, you know **100%** that your server is being snooped on. You can use server-level tools (like `Auditd` on Linux) to notify you the instant these files are opened, giving you an early warning before they find your real data.

---

## 📜 Principles followed
1. **Deny by Default:** Total access control logic.
2. **Data vs Logic:** Treating user input as "Dumb Strings."
3. **Fail-Safe Defaults:** Systems fail in a "Closed" state.
4. **No Glassmorphism:** Clean, professional, and accessible UI design.
