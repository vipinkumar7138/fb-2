from flask import Blueprint, request, jsonify, render_template
import requests

uid_extractor_bp = Blueprint('uid_extractor', __name__)

# ग्लोबल वेरिएबल्स
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
}

@uid_extractor_bp.route('/')
def uid_extractor():
    return render_template('uid_extractor.html')

@uid_extractor_bp.route('/validate_token', methods=['POST'])
def validate_token():
    try:
        access_token = request.json.get('access_token')
        if not access_token:
            return jsonify({'error': {'message': 'No token provided'}})
        
        response = requests.get(
            f'https://graph.facebook.com/me?fields=name,id&access_token={access_token}',
            timeout=10
        )
        
        if response.status_code != 200:
            error_data = response.json()
            return jsonify({
                'error': {
                    'message': 'Invalid or expired token',
                    'details': error_data.get('error', {}).get('message', 'Unknown error')
                }
            })
        
        return jsonify(response.json())
        
    except requests.exceptions.Timeout:
        return jsonify({'error': {'message': 'Request timed out. Try again.'}})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}})

@uid_extractor_bp.route('/get_messenger_chats', methods=['POST'])
def get_messenger_chats():
    try:
        access_token = request.json.get('access_token')
        if not access_token:
            return jsonify({'error': 'No access token provided'})
        
        response = requests.get(
            f'https://graph.facebook.com/me/conversations?fields=participants,name&access_token={access_token}',
            timeout=30
        )
        
        if response.status_code != 200:
            error_data = response.json()
            return jsonify({
                'error': {
                    'message': 'Invalid access token',
                    'details': error_data.get('error', {}).get('message', 'Unknown error')
                }
            })
        
        chats = []
        for chat in response.json().get('data', []):
            chat_name = chat.get('name') or ', '.join(
                [p['name'] for p in chat.get('participants', {}).get('data', [])]
            )
            chats.append({
                'id': chat['id'],
                'name': chat_name
            })
            
        return jsonify({'chats': chats})
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. Please try again.'})
    except Exception as e:
        return jsonify({'error': str(e)})

@uid_extractor_bp.route('/get_posts', methods=['POST'])
def get_posts():
    try:
        access_token = request.json.get('access_token')
        if not access_token:
            return jsonify({'error': 'No access token provided'})
        
        response = requests.get(
            f'https://graph.facebook.com/me/feed?fields=id,message,from&limit=20&access_token={access_token}',
            timeout=30
        )
        
        if response.status_code != 200:
            error_data = response.json()
            return jsonify({
                'error': {
                    'message': 'Invalid access token',
                    'details': error_data.get('error', {}).get('message', 'Unknown error')
                }
            })
        
        posts = []
        for post in response.json().get('data', []):
            posts.append({
                'id': post['id'],
                'name': post.get('message', 'No text content'),
                'profile_name': post.get('from', {}).get('name', 'Unknown')
            })
            
        return jsonify({'posts': posts})
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. Please try again.'})
    except Exception as e:
        return jsonify({'error': str(e)})
