from flask import Blueprint, request
from threading import Thread, Event
import time
import random
import requests

auto_reply_blueprint = Blueprint('auto_reply', __name__)

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
}

auto_reply_settings = {
    'active': False,
    'stop_event': Event()
}

@auto_reply_blueprint.route('/set_auto_reply', methods=['POST'])
def set_auto_reply():
    try:
        access_token = request.form.get('auto_reply_token')
        keyword = request.form.get('keyword')
        reply_mode = request.form.get('reply_mode')
        group_ids = request.form.get('group_ids', '').split(',') if request.form.get('group_ids') else []
        
        messages_file = request.files['messages_file']
        messages = messages_file.read().decode().splitlines()
        
        auto_reply_settings.update({
            'access_token': access_token,
            'keyword': keyword,
            'messages': messages,
            'reply_mode': reply_mode,
            'group_ids': [gid.strip() for gid in group_ids if gid.strip()],
            'active': False,
            'stop_event': Event()
        })
        
        return "ऑटो रिप्लाई सेटिंग्स सफलतापूर्वक सेव की गईं!"
    
    except Exception as e:
        return f"त्रुटि: {str(e)}", 400

@auto_reply_blueprint.route('/start_auto_reply', methods=['POST'])
def start_auto_reply():
    if not auto_reply_settings or 'access_token' not in auto_reply_settings:
        return "ऑटो रिप्लाई सेटिंग्स कॉन्फ़िगर नहीं की गई हैं", 400
    
    if auto_reply_settings.get('active', False):
        return "ऑटो रिप्लाई पहले से चल रहा है", 200
    
    auto_reply_settings['active'] = True
    auto_reply_settings['stop_event'].clear()
    
    thread = Thread(target=run_auto_reply, args=(auto_reply_settings,))
    thread.start()
    
    return "ऑटो रिप्लाई सफलतापूर्वक शुरू हो गया"

@auto_reply_blueprint.route('/stop_auto_reply', methods=['POST'])
def stop_auto_reply():
    if not auto_reply_settings:
        return "ऑटो रिप्लाई सेटिंग्स कॉन्फ़िगर नहीं की गई हैं", 400
    
    if not auto_reply_settings.get('active', False):
        return "ऑटो रिप्लाई चल नहीं रहा है", 200
    
    auto_reply_settings['active'] = False
    auto_reply_settings['stop_event'].set()
    
    return "ऑटो रिप्लाई सफलतापूर्वक रोक दिया गया"

def run_auto_reply(settings):
    access_token = settings['access_token']
    keyword = settings['keyword']
    messages = settings['messages']
    reply_mode = settings['reply_mode']
    group_ids = settings['group_ids']
    stop_event = settings['stop_event']
    
    while not stop_event.is_set() and settings['active']:
        try:
            response = requests.get(
                f'https://graph.facebook.com/me/conversations?fields=participants,messages{{message}}&access_token={access_token}',
                timeout=30
            )
            
            if response.status_code != 200:
                time.sleep(60)
                continue
            
            conversations = response.json().get('data', [])
            
            for conv in conversations:
                if stop_event.is_set() or not settings['active']:
                    break
                
                conv_id = conv['id']
                
                if reply_mode == 'exclude' and conv_id in group_ids:
                    continue
                if reply_mode == 'include' and conv_id not in group_ids:
                    continue
                
                messages_data = conv.get('messages', {}).get('data', [])
                if not messages_data:
                    continue
                
                last_message = messages_data[0].get('message', '')
                if keyword.lower() in last_message.lower():
                    reply_msg = random.choice(messages)
                    api_url = f'https://graph.facebook.com/v15.0/t_{conv_id}/'
                    parameters = {'access_token': access_token, 'message': reply_msg}
                    
                    response = requests.post(api_url, data=parameters, headers=headers)
                    
                    time.sleep(5)
            
            time.sleep(30)
            
        except Exception as e:
            time.sleep(60)
