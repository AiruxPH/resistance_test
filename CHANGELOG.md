# Changelog - Resistance Test Project

All notable changes to this project will be documented in this file.

## [2026-03-12] - Initial Release

### Added
- **Project Structure:** Created initialization files including `index.html`, `style.css`, and `app.js`.
- **Premium UI:** Implemented a dark-themed, high-performance dashboard for security testing. Adhered to "No Glassmorphism" rule.
- **Resistance Testing Engine:** Created `tester.py` using Python's `requests` library to perform vulnerability scans.
- **Security Modules:**
  - **A02:** Cryptographic Failure (HTTPS check).
  - **A03:** Injection (XSS/SQLi probes).
  - **A05:** Security Misconfiguration (Sensitive file scan).
  - **A10:** SSRF probing.
- **Dependency Management:** Installed `requests` library via pip to support the testing engine.
- **Task & Plan Artifacts:** Created `task.md`, `implementation_plan.md`, and `walkthrough.md` for project tracking and documentation.

## [2026-03-12] - Bridge Integration

### Added
- **Backend Server:** Created `server.py` using Flask to act as a bridge between the frontend and the testing engine.
- **Real-time Integration:** Updated `app.js` to fetch real results from the local Python server instead of using simulations.
- **CORS Support:** Integrated `flask-cors` for secure local communication.

## [2026-03-12] - A07 Brute Force Implementation

### Added
- **A07 Module:** Implemented automated Brute Force resistance testing in `tester.py`.
- **Safety Kill-Switches:** Added automatic detection of HTTP 429 and 403 status codes to abort tests and prevent IP banning.
- **Aggressive Mode Toggle:** Added a UI checkbox to switch between "Safe" (5 attempts) and "Aggressive" (20 attempts) testing.
- **Throttling:** Implemented time delays between probes to ensure ethical testing behavior.

## [2026-03-12] - Honey-Token Generator (Forensic Traps)

### Added
- **Canary Engine:** Created `canary_gen.py` to generate decoy environment files, database configs, and password lists.
- **Forensic UI:** Added a new "Forensic Traps" section to the dashboard with one-click generation buttons.
- **Bridge Endpoint:** Added `/generate-trap` to `server.py` to serve decoy content to the frontend.
- **Live Preview:** Updated `app.js` to stream decoy content directly into the dashboard console for immediate use.

## [2026-03-12] - GitHub Release Preparation

### Added
- **README.md:** Comprehensive documentation on project features, quick start guide, and security principles.
- **run.py:** Automated "all-in-one" script that installs dependencies, launches the backend, and opens the frontend.
- **requirements.txt:** Standardized dependency list for easy setup.

## [2026-03-12] - Professional Refactoring & Portability

### Changed
- **Folder Structure:** Reorganized project into `core/` (logic) and `ui/` (frontend) for professional separation of concerns.
- **Dynamic Hosting:** Updated `app.js` and `server.py` to automatically detect the host, enabling deployment on any server/port.
- **One-Click Experience:** Modified `server.py` to serve the UI assets directly, reducing the number of open ports required.

### Added
- **start.bat (Windows Bootstrap):** Added a batch script that checks for Python/Pip and provides friendly guidance if they are missing.
- **Enhanced Launcher:** Updated `run.py` to handle the new directory structure and provide a smoother setup flow.

### Fixed
- **Console Crash:** Resolved an issue where the frontend would crash with a `toLowerCase` error due to a field name mismatch (`status` vs `level`) between the Python engine and JavaScript.
- **Defensive Logging:** Added fallback mechanisms in `app.js` to handle malformed log entries without interrupting the test sequence.

## [2026-03-12] - Final Polish & Legal Compliance


### Changed
- **README.md Refinement:** Added detailed legal disclaimers, ethical use guidelines, and multi-OS installation instructions.
- **UI Enhancements:** Integrated a prominent safety warning in the dashboard footer to emphasize authorized use only.
- **Documentation:** Finalized the internal project artifacts and structure documentation for GitHub consistency.



## [2026-03-12] - Database Hardening Module

### Added
- **DB Hardening Check:** New module in `tester.py` that verifies public `/database/` folder accessibility (User Rule #5).
- **Remote SQL Probe:** Integrated port-level monitoring for MySQL (3306) to verify Rule #8 remote access hardening.
- **Dependency Update:** Added `pymysql` to `requirements.txt` for future database-level probing.
- **UI Interaction:** Seamlessly integrated the DB Hardening toggle into the Dashboard.





