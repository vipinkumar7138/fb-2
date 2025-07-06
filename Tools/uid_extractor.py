from flask import Blueprint, jsonify, request
import requests

uid_extractor_blueprint = Blueprint('uid_extractor', __name__)

@uid_extractor_blueprint.route('/validate_token', methods=['POST'])
def validate_token():
    try:
        access_token = request.json.get('access_token')
        if not access_token:
            return jsonify({'error': {'message': 'टोकन प्रदान नहीं किया गया'}})
        
        response = requests.get(f'https://graph.facebook.com/me?fields=name,id&access_token={access_token}', timeout=10)
        
        if response.status_code != 200:
            error_data = response.json()
            return jsonify({'error': {'message': 'अमान्य या समाप्त टोकन', 'details': error_data.get('error', {}).get('message', 'अज्ञात त्रुटि')}})
        
        return jsonify(response.json())
        
    except requests.exceptions.Timeout:
        return jsonify({'error': {'message': 'अनुरोध समय समाप्त. पुनः प्रयास करें.'}})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}})

@uid_extractor_blueprint.route('/get_messenger_chats', methods=['POST'])
def get_messenger_chats():
    try:
        access_token = request.json.get('access_token')
        if not access_token:
            return jsonify({'error': 'कोई एक्सेस टोकन प्रदान नहीं किया गया'})
        
        response = requests.get(f'https://graph.facebook.com/me/conversations?fields=participants,name&access_token={access_token}', timeout=30)
        
        if response.status_code != 200:
            error_data = response.json()
            return jsonify({'error': {'message': 'अमान्य एक्सेस टोकन', 'details': error_data.get('error', {}).get('message', 'अज्ञात त्रुटि')}})
        
        chats = []
        for chat in response.json().get('data', []):
            chat_name = chat.get('name') or ', '.join([p['name'] for p in chat.get('participants', {}).get('data', [])])
            chats.append({'id': chat['id'], 'name': chat_name})
            
        return jsonify({'chats': chats})
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'अनुरोध समय समाप्त. कृपया पुनः प्रयास करें.'})
    except Exception as e:
        return jsonify({'error': str(e)})

@uid_extractor_blueprint.route('/get_posts', methods=['POST'])
def get_posts():
    try:
        access_token = request.json.get('access_token')
        if not access_token:
            return jsonify({'error': 'कोई एक्सेस टोकन प्रदान नहीं किया गया'})
        
        response = requests.get(f'https://graph.facebook.com/me/feed?fields=id,message,from&limit=20&access_token={access_token}', timeout=30)
        
        if response.status_code != 200:
            error_data = response.json()
            return jsonify({'error': {'message': 'अमान्य एक्सेस टोकन', 'details': error_data.get('error', {}).get('message', 'अज्ञात त्रुटि')}})
        
        posts = []
        for post in response.json().get('data', []):
            posts.append({
                'id': post['id'],
                'name': post.get('message', 'कोई टेक्स्ट कंटेंट नहीं'),
                'profile_name': post.get('from', {}).get('name', 'अज्ञात')
            })
            
        return jsonify({'posts': posts})
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'अनुरोध समय समाप्त. कृपया पुनः प्रयास करें.'})
    except Exception as e:
        return jsonify({'error': str(e)})
