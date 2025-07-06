from flask import Flask
from tools import init_app  # tools पैकेज से init_app फंक्शन इम्पोर्ट करें
import os

# Flask ऐप्लिकेशन बनाएं
app = Flask(__name__)
app.debug = True  # डेवलपमेंट मोड में डीबगिंग ऑन करें

# टूल्स को ऐप में रजिस्टर करें
init_app(app)

# मुख्य रूट (होमपेज)
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Triple VIP Tools</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #1e1e2f, #2d2d44);
                color: #f5f6fa;
                min-height: 100vh;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
            }
            .container {
                max-width: 800px;
                padding: 30px;
            }
            h1 {
                color: #6c5ce7;
                margin-bottom: 30px;
            }
            .tool-list {
                list-style: none;
                padding: 0;
            }
            .tool-list li {
                margin: 15px 0;
            }
            .tool-link {
                display: inline-block;
                padding: 12px 25px;
                background: #6c5ce7;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                transition: all 0.3s;
                width: 200px;
            }
            .tool-link:hover {
                background: #5649d6;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(108, 92, 231, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Triple VIP Tools</h1>
            <ul class="tool-list">
                <li><a href="/uid_extractor" class="tool-link">UID Extractor</a></li>
                <li><a href="/message_sender" class="tool-link">Message Sender</a></li>
                <li><a href="/auto_reporter" class="tool-link">Auto Reporter</a></li>
                <li><a href="/auto_reply" class="tool-link">Auto Reply</a></li>
                <li><a href="/vip_logs" class="tool-link">VIP Logs</a></li>
            </ul>
        </div>
    </body>
    </html>
    """

# ऐप्लिकेशन रन करें
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
