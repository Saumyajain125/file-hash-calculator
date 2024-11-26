from flask import Flask, render_template, request, jsonify, send_from_directory
import hashlib
import os
import tempfile

app = Flask(__name__)

# Serve static files from the templates directory
@app.route('/')
def index():
    return send_from_directory('../templates', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        hash_md5 = hashlib.md5()
        
        # Process the file in chunks directly from the request stream
        chunk_size = 4096
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            hash_md5.update(chunk)
        
        return jsonify({
            'filename': file.filename,
            'hash': hash_md5.hexdigest()
        })

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 