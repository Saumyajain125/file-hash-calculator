from flask import Flask, render_template, request, jsonify
import hashlib
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def calculate_hash(file_path):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 