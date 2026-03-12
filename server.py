from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import json
import os
import sys

# Add core to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
import core.canary_gen as canary_gen

app = Flask(__name__, static_folder='ui')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('ui', 'index.html')

@app.route('/<path:path>')
def serve_ui(path):
    return send_from_directory('ui', path)

@app.route('/test', methods=['POST'])
def run_test():
    data = request.json
    target_url = data.get('url')
    is_aggressive = data.get('aggressive', False)
    
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Run the tester.py script in the core folder
        tester_path = os.path.join('core', 'tester.py')
        cmd = [sys.executable, tester_path, target_url]
        if is_aggressive:
            cmd.append('--aggressive')

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        output_lines = result.stdout.strip().split('\n')
        logs = []
        final_score = "0%"
        
        for line in output_lines:
            try:
                log_data = json.loads(line)
                logs.append(log_data)
                if log_data.get('module') == "SUMMARY":
                    final_score = log_data.get('message').split(': ')[1]
            except json.JSONDecodeError:
                continue
                
        return jsonify({
            "logs": logs,
            "score": final_score
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-trap', methods=['POST'])
def generate_trap():
    data = request.json
    trap_type = data.get('type')
    
    content = ""
    filename = ""

    if trap_type == 'env':
        content = canary_gen.generate_env()
        filename = ".env.decoy"
    elif trap_type == 'db':
        content = canary_gen.generate_db_config()
        filename = "config_db.php"
    elif trap_type == 'txt':
        content = canary_gen.generate_passwords_txt()
        filename = "passwords.txt"
    else:
        return jsonify({"error": "Invalid trap type"}), 400

    return jsonify({
        "content": content,
        "filename": filename
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Resistance Test Backend Server running on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port)
