import os
import qrcode
import random
import string
import signal
import sys
import atexit
from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from utils import get_local_ip

PORT = random.randint(1000, 9999)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

LOCAL_IP = get_local_ip()

# Generate a random folder name for each user session
def generate_session_id(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        session_id = generate_session_id()
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(user_folder, exist_ok=True)

        file_path = os.path.join(user_folder, file.filename)
        file.save(file_path)

        # Create QR code for the file download URL
        url = f'http://{LOCAL_IP}:{PORT}/file/{session_id}/{file.filename}'
        qr = qrcode.make(url)
        qr_path = os.path.join('static', 'qrcode.png')
        qr.save(qr_path)

        return redirect(url_for('uploaded', session=session_id, filename=file.filename))
    return 'File not found', 400

@app.route('/uploaded/<session>/<filename>')
def uploaded(session, filename):
    return f'''
    <html>
    <head>
        <title>Upload Successful ✅</title>
        <style>
            body {{
                background: linear-gradient(135deg, #e0f7fa, #f0f4c3);
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
                max-width: 90%;
                width: 400px;
            }}
            .success {{
                font-size: 22px;
                color: #388e3c;
                margin-bottom: 10px;
            }}
            .filename {{
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 20px;
            }}
            .qr-img {{
                width: 250px;
                margin: 20px auto;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            .download-link {{
                display: inline-block;
                margin-top: 30px;
                padding: 14px 28px;
                font-size: 18px;
                text-decoration: none;
                background-color: #007bff;
                color: white;
                border-radius: 10px;
                transition: 0.3s;
            }}
            .download-link:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success">✅ Upload successful!</div>
            <div class="filename">{filename}</div>
            <p>📲 Scan the QR code below:</p>
            <img src="/static/qrcode.png" alt="QR Code" class="qr-img" />
            <br>
            <a class="download-link" href="/file/{session}/{filename}">📥 Download</a>
        </div>
    </body>
    </html>
    '''

@app.route('/file/<session>/<filename>')
def download_file(session, filename):
    folder = os.path.join(app.config['UPLOAD_FOLDER'], session)
    return send_from_directory(folder, filename, as_attachment=True)

def cleanup_uploads():
    folder = app.config['UPLOAD_FOLDER']
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        print("📛 uploads/ folder files deleted.")

def handle_exit(sig, frame):
    cleanup_uploads()
    sys.exit(0)

# Handle process termination signals
signal.signal(signal.SIGINT, handle_exit)   # Ctrl+C
signal.signal(signal.SIGTERM, handle_exit)  # Kill signal
atexit.register(cleanup_uploads)            # Clean on natural exit

if __name__ == '__main__':
    print(f"📡 Open your browser at: http://8.8.8.8:{PORT}")
    app.run(host='0.0.0.0', port=PORT)
