from flask import Flask
from tools.uid_extractor import uid_extractor_bp
from tools.message_sender import message_sender_bp
from tools.auto_reporter import auto_reporter_bp
from tools.auto_reply import auto_reply_bp
from tools.vip_logs import vip_logs_bp
import os

app = Flask(__name__)
app.debug = True

# Blueprints रजिस्टर करें
app.register_blueprint(uid_extractor_bp, url_prefix='/uid_extractor')
app.register_blueprint(message_sender_bp, url_prefix='/message_sender')
app.register_blueprint(auto_reporter_bp, url_prefix='/auto_reporter')
app.register_blueprint(auto_reply_bp, url_prefix='/auto_reply')
app.register_blueprint(vip_logs_bp, url_prefix='/vip_logs')

@app.route('/')
def home():
    return """
    <h1>Triple VIP Tools</h1>
    <ul>
        <li><a href="/uid_extractor">UID Extractor</a></li>
        <li><a href="/message_sender">Message Sender</a></li>
        <li><a href="/auto_reporter">Auto Reporter</a></li>
        <li><a href="/auto_reply">Auto Reply</a></li>
        <li><a href="/vip_logs">VIP Logs</a></li>
    </ul>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
