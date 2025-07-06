from flask import Blueprint, request
from threading import Thread, Event
import time
import random
import string
import requests

message_sender_bp = Blueprint('message_sender', __name__)

# ग्लोबल वेरिएबल्स
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
}
stop_events = {}
threads = {}

@message_sender_bp.route('/')
def message_sender():
    return render_template('message_sender.html')

@message_sender_bp.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        uid_option = request.form.get('uidOption')

        # Load tokens
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        # Load UIDs
        if uid_option == 'single':
            thread_ids = [request.form.get('threadId')]
        else:
            uid_file = request.files['uidFile']
            thread_ids = uid_file.read().decode().strip().splitlines()

        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        password = request.form.get('mmm')
        mmm = requests.get('https://pastebin.com/raw/tn5e8Ub9').text.strip()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_ids, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'

def send_messages(access_tokens, thread_ids, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                for thread_id in thread_ids:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = str(mn) + ' ' + message1
                    parameters = {'access_token': access_token, 'message': message}
                    try:
                        response = requests.post(api_url, data=parameters, headers=headers)
                    except Exception as e:
                        continue
                    time.sleep(time_interval)

@message_sender_bp.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'
