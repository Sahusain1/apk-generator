from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate-apk', methods=['POST'])
def generate_apk():
    data = request.json
    
    app_name = data.get('appName', 'MyWebApp')
    version_name = data.get('versionName', '1.0.0')
    
    print(f"Building APK for: {app_name} (v{version_name})")
    
    return jsonify({
        "status": "success",
        "message": "Build process started successfully!",
        "download_url": f"#"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
