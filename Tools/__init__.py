# facebook_tools/tools/__init__.py

from .uid_extractor import uid_extractor_bp
from .message_sender import message_sender_bp
from .auto_reporter import auto_reporter_bp
from .auto_reply import auto_reply_bp
from .vip_logs import vip_logs_bp

# Initialize global variables that need to be shared across blueprints
stop_events = {}
threads = {}
report_stop_events = {}
report_threads = {}
auto_reply_settings = {
    'active': False,
    'stop_event': None,  # Will be initialized when needed
    'access_token': None,
    'keyword': None,
    'messages': [],
    'reply_mode': 'all',
    'group_ids': []
}
logs = []

# Common headers for API requests
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
}

def init_app(app):
    """Initialize all tool blueprints with the Flask app"""
    app.register_blueprint(uid_extractor_bp, url_prefix='/uid_extractor')
    app.register_blueprint(message_sender_bp, url_prefix='/message_sender')
    app.register_blueprint(auto_reporter_bp, url_prefix='/auto_reporter')
    app.register_blueprint(auto_reply_bp, url_prefix='/auto_reply')
    app.register_blueprint(vip_logs_bp, url_prefix='/vip_logs')
    
    # Initialize the stop event for auto reply
    auto_reply_settings['stop_event'] = threading.Event()

def add_log(action, status, details):
    """Common logging function for all tools"""
    import datetime
    log_entry = {
        "timestamp": str(datetime.datetime.now()),
        "action": action,
        "status": status,
        "details": details
    }
    logs.append(log_entry)
    # Save to file (optional)
    with open("logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# Import required modules that will be used by multiple blueprints
import threading
import json
import time
import random
import string
import requests
from flask import make_response
from io import StringIO
import csv
