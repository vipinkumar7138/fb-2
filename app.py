from flask import Flask, render_template
from tools.uid_extractor import uid_extractor_blueprint
from tools.message_sender import message_sender_blueprint
from tools.auto_reporter import auto_reporter_blueprint
from tools.auto_reply import auto_reply_blueprint
from tools.vip_logs import vip_logs_blueprint

app = Flask(__name__)
app.debug = True

# ब्लूप्रिंट्स रजिस्टर करें
app.register_blueprint(uid_extractor_blueprint)
app.register_blueprint(message_sender_blueprint)
app.register_blueprint(auto_reporter_blueprint)
app.register_blueprint(auto_reply_blueprint)
app.register_blueprint(vip_logs_blueprint)

@app.route('/')
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
