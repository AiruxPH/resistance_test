import subprocess
import sys
import os
import webbrowser
import time

def install_requirements():
    print("[*] Checking dependencies...")
    try:
        import flask
        import flask_cors
        import requests
        import pymysql
        print("[+] All dependencies are already installed.")
    except ImportError:
        print("[!] Missing dependencies. Installing from requirements.txt...")
        if not os.path.exists("requirements.txt"):
            print("[-] Error: requirements.txt not found.")
            sys.exit(1)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("[+] Installation successful.")
        except subprocess.CalledProcessError as e:
            print(f"[-] Failed to install dependencies: {e}")
            print("\n[TIP] Try running your terminal as Administrator.")
            sys.exit(1)

def run_server():
    print("[*] Starting Resistance Test Backend Server...")
    try:
        # Run server.py from root
        server_process = subprocess.Popen([sys.executable, "server.py"])
        return server_process
    except Exception as e:
        print(f"[-] Failed to start server: {e}")
        sys.exit(1)

def main():
    # 1. Ensure we are in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 2. Check and install requirements
    install_requirements()

    # 3. Start the server
    server = run_server()

    # 4. Open the UI
    # Now that server.py serves the UI, we point to the URL
    time.sleep(2) # Give server a moment to boot
    url = "http://127.0.0.1:5000"
    print(f"[*] Opening Dashboard UI at {url}...")
    webbrowser.open(url)

    print("\n" + "="*50)
    print("RESISTANCE TEST IS NOW RUNNING")
    print("Address: " + url)
    print("="*50)
    print("\nPress Ctrl+C to stop the server.")

    try:
        # Keep the script alive so the server process doesn't die immediately
        while True:
            if server.poll() is not None:
                print("[-] Server process died unexpectedly.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Stopping server...")
        server.terminate()
        print("[+] Goodbye!")

if __name__ == "__main__":
    main()
