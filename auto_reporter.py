from flask import Blueprint, request
from threading import Thread, Event
import time
import random
import string
import requests

auto_reporter_bp = Blueprint('auto_reporter', __name__)

# ग्लोबल वेरिएबल्स
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
}
report_stop_events = {}
report_threads = {}

@auto_reporter_bp.route('/')
def auto_reporter():
    return render_template('auto_reporter.html')

@auto_reporter_bp.route('/start_reporting', methods=['POST'])
def start_reporting():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')

        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        target_id = request.form.get('targetId')
        report_reason = request.form.get('reportReason')
        time_interval = int(request.form.get('time'))
        report_count = int(request.form.get('reportCount'))

        password = request.form.get('mmm')
        mmm = requests.get('https://pastebin.com/raw/tn5e8Ub9').text.strip()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        report_stop_events[task_id] = Event()
        thread = Thread(target=send_reports, args=(access_tokens, target_id, report_reason, time_interval, report_count, task_id))
        report_threads[task_id] = thread
        thread.start()

        return f'Reporting task started with ID: {task_id}'

@auto_reporter_bp.route('/stop_reporting', methods=['POST'])
def stop_reporting():
    task_id = request.form.get('taskId')
    if task_id in report_stop_events:
        report_stop_events[task_id].set()
        return f'Reporting task with ID {task_id} has been stopped.'
    else:
        return f'No reporting task found with ID {task_id}.'

def send_reports(access_tokens, target_id, report_reason, time_interval, report_count, task_id):
    stop_event = report_stop_events[task_id]
    reports_sent = 0
    
    while not stop_event.is_set() and reports_sent < report_count:
        for access_token in access_tokens:
            if stop_event.is_set() or reports_sent >= report_count:
                break
                
            try:
                object_id = target_id
                if 'facebook.com' in target_id:
                    object_id = target_id.split('/')[-1].split('?')[0]
                
                api_url = f'https://graph.facebook.com/v15.0/{object_id}/reports'
                parameters = {
                    'access_token': access_token,
                    'reason': report_reason
                }
                
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    reports_sent += 1
                
                time.sleep(time_interval)
                
            except Exception as e:
                continue
