import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Apne GitHub repository ki details yahan set karein
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN")
REPO_OWNER = "Sahusain1"
REPO_NAME = "apk-generator"

@app.route('/generate-apk', methods=['POST'])
def generate_apk():
    try:
        data = request.json or {}
        app_name = data.get('appName', 'MyWebApp')
        app_url = data.get('appUrl', 'https://google.com')
        version_name = data.get('versionName', '1.0.0')

        # Trigger GitHub Actions Workflow
        github_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        payload = {
            "event_type": "build-apk",
            "client_payload": {
                "appName": app_name,
                "appUrl": app_url,
                "versionName": version_name
            }
        }

        response = requests.post(github_url, json=payload, headers=headers)

        if response.status_code in [200, 204]:
            return jsonify({
                "status": "success",
                "message": "Real APK Compilation Started on Cloud!",
                "download_url": f"https://github.com/{REPO_OWNER}/{REPO_NAME}/actions"
            })
        else:
            return jsonify({"status": "error", "message": response.text}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
