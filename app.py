from flask import Flask, render_template, request, send_file, jsonify
import requests
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_song():
    data = request.json
    spotify_url = data.get('url')
    
    if not spotify_url:
        return jsonify({"error": "Please provide a valid URL"}), 400

    api_url = "https://spotdown.org/api/download"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    payload = {"url": spotify_url}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            return send_file(
                io.BytesIO(response.content),
                mimetype='audio/mpeg',
                as_attachment=True,
                download_name="Saiful_Islam_Downloader.mp3"
            )
        else:
            return jsonify({"error": "Failed to fetch song"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

