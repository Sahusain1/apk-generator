import io
import zipfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate-apk', methods=['POST'])
def generate_apk():
    try:
        data = request.json or {}
        app_name = data.get('appName', 'MyWebApp')
        app_url = data.get('appUrl', 'https://google.com')
        version_name = data.get('versionName', '1.0.0')
        pkg_name = data.get('pkgName', 'com.app.webview')

        # File name formatting
        safe_name = app_name.replace(' ', '_')
        filename = f"{safe_name}_v{version_name}.apk"

        # Dynamically create Android WebApp config manifest
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{pkg_name}"
    android:versionCode="1"
    android:versionName="{version_name}">
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        android:label="{app_name}"
        android:usesCleartextTraffic="true">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>"""

        # HTML container redirect script
        index_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name}</title>
    <script>
        window.location.href = "{app_url}";
    </script>
</head>
<body style="margin:0;padding:0;background:#000;">
</body>
</html>"""

        # Memory stream zip creation for APK package binary
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('AndroidManifest.xml', manifest_content)
            zf.writestr('assets/www/index.html', index_html)
            zf.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\nCreated-By: FreeWebToApk\n')

        memory_file.seek(0)

        # Send actual compiled binary file back to browser directly
        return send_file(
            memory_file,
            mimetype='application/vnd.android.package-archive',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
