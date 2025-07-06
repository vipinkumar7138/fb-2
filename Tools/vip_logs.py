from flask import Blueprint, jsonify, make_response
from io import StringIO
import csv
import datetime
import json

vip_logs_bp = Blueprint('vip_logs', __name__)

logs = []

@vip_logs_bp.route('/')
def vip_logs():
    return render_template('vip_logs.html')

@vip_logs_bp.route('/get_logs')
def get_logs():
    return jsonify({"logs": logs})

@vip_logs_bp.route('/download_logs')
def download_logs():
    # Create CSV data
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(["Timestamp", "Action", "Status", "Details"])
    
    for log in logs:
        writer.writerow([log['timestamp'], log['action'], log['status'], log['details']])
    
    response = make_response(csv_data.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=vip_logs.csv"
    response.headers["Content-type"] = "text/csv"
    return response

def add_log(action, status, details):
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
