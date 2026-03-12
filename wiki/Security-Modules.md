# Security Modules: Deep Dive 🧠

Resistance Test v1.0.0 covers the most critical automated segments of the **OWASP Top 10**.

## 🔴 A01: Broken Access Control
- **Probe:** Scans for unprotected administrative directories and API endpoints.
- **Risk:** Unauthorized users accessing sensitive data or control panels.

## 🟠 A02: Cryptographic Failures
- **Probe:** Verifies HTTPS protocol and TLS enforcement.
- **Risk:** "Man-in-the-Middle" attacks where data is stolen in transit.

## 🟡 A03: Injection Probes
- **Probe:** Tests for XSS (Cross-Site Scripting) and basic SQL Injection reflection.
- **Risk:** Hackers running malicious code on your users' browsers.

## 🔴 A05: Security Misconfiguration
- **Probe:** Scans for exposed `.env`, `.git/config`, and server info files.
- **Risk:** Direct exposure of database passwords and secret keys.

## 🟠 A06: Vulnerable & Outdated Components
- **Probe:** Analyzes server headers (`Server`, `X-Powered-By`) for version leaks.
- **Risk:** Hackers finding targeted exploits for specific software versions.

## 🟡 A07: Identification & Auth Failures
- **Probe:** Intelligent brute-force detection that identifies real login paths.
- **Risk:** Account takeover through automated password guessing.

## 🟠 A08: Software & Data Integrity
- **Probe:** Scans for exposed CI/CD pipelines and deployment metadata.
- **Risk:** Exposing the "Internal Blueprints" of your infrastructure.

## 🔴 A09: Security Logging & Monitoring
- **Probe:** Looks for publicly readable technical logs (`error.log`, `access.log`).
- **Risk:** Giving hackers a map of your system errors and user activity.

## 🟡 A10: Server-Side Request Forgery (SSRF)
- **Probe:** Basic probing for URL-based internal redirection risks.
- **Risk:** Hackers using your server to attack your internal network.
