from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

@app.route('/')
def index():
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Hash Calculator</title>
    <style>
        body {
            background-color: #0a0a0a;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background-color: #1a1a1a;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
            max-width: 600px;
            width: 100%;
            position: relative;
        }

        .cursor-tag {
            position: absolute;
            top: -15px;
            right: -15px;
            background: #00ff00;
            color: #000;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.8em;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
            transform: rotate(5deg);
            z-index: 100;
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        }

        .upload-area {
            border: 2px dashed #00ff00;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .upload-area:hover {
            background-color: rgba(0, 255, 0, 0.1);
        }

        .result {
            background-color: #000;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            display: none;
        }

        .hash {
            word-break: break-all;
            font-size: 0.9em;
            margin-top: 10px;
        }

        .filename {
            color: #00cc00;
            margin-bottom: 5px;
        }

        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }

        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 1; }
        }

        .blink {
            animation: blink 1s infinite;
        }

        #file-input {
            display: none;
        }

        .error {
            color: #ff0000;
            margin-top: 10px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="cursor-tag">Made with Cursor in <10min</div>
        <h1>[ FILE HASH CALCULATOR ]</h1>
        
        <div class="upload-area" id="drop-zone">
            <p>DROP FILE HERE</p>
            <p>or</p>
            <p>CLICK TO SELECT</p>
        </div>
        
        <input type="file" id="file-input">
        
        <div class="loading">
            <p class="blink">CALCULATING HASH...</p>
        </div>
        
        <div class="error">
            ERROR PROCESSING FILE
        </div>
        
        <div class="result">
            <div class="filename"></div>
            <div class="hash"></div>
        </div>
    </div>

    <script>
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('file-input');
        const result = document.querySelector('.result');
        const loading = document.querySelector('.loading');
        const error = document.querySelector('.error');

        dropZone.addEventListener('click', () => fileInput.click());

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.style.backgroundColor = 'rgba(0, 255, 0, 0.1)';
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.style.backgroundColor = '';
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.style.backgroundColor = '';
            const file = e.dataTransfer.files[0];
            processFile(file);
        });

        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            processFile(file);
        });

        function processFile(file) {
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            result.style.display = 'none';
            error.style.display = 'none';
            loading.style.display = 'block';

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                if (data.error) {
                    error.style.display = 'block';
                    return;
                }
                result.querySelector('.filename').textContent = `FILE: ${data.filename}`;
                result.querySelector('.hash').textContent = `MD5: ${data.hash}`;
                result.style.display = 'block';
            })
            .catch(() => {
                loading.style.display = 'none';
                error.style.display = 'block';
            });
        }
    </script>
</body>
</html>
    '''
    return html_content

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