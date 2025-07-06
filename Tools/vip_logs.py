from flask import Blueprint, make_response
from io import StringIO
import csv
import datetime

vip_logs_blueprint = Blueprint('vip_logs', __name__)

logs = []

def add_log(action, status, details):
    log_entry = {
        "timestamp": str(datetime.datetime.now()),
        "action": action,
        "status": status,
        "details": details
    }
    logs.append(log_entry)

@vip_logs_blueprint.route('/get_logs')
def get_logs():
    return {"logs": logs}

@vip_logs_blueprint.route('/download_logs')
def download_logs():
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(["Timestamp", "Action", "Status", "Details"])
    
    for log in logs:
        writer.writerow([log['timestamp'], log['action'], log['status'], log['details']])
    
    response = make_response(csv_data.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=vip_logs.csv"
    response.headers["Content-type"] = "text/csv"
    return response
