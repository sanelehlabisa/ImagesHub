from flask import request, jsonify # type: ignore
import requests
from classes.user import User
from classes.database import Database
import os
from dotenv import load_dotenv

def get_users() -> tuple:
    """
    Description: Handling the GET /api/v2/users endpoint.
    Input: Query parameters ('min_id', 'max_id', or 'limit'), or nothing.
    Output: JSON of list of User objects or 'message' key describing reason for process failure.
    """

    load_dotenv()
    db = Database()
    table_name = 'user'
    users = []

    # Get query parameters
    min_id = request.args.get('min_id', type=int)
    max_id = request.args.get('max_id', type=int)
    limit = request.args.get('limit', type=int)

    try:
        if min_id is not None and max_id is not None:
            for user in db.read_range(table_name, min_id, max_id):
                users.append(User(*user).toJSON())
        elif limit is not None:
            for user in db.read(table_name, limit=limit):
                users.append(User(*user).toJSON())
        else:
            for user in db.read(table_name):
                users.append(User(*user).toJSON())
        
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
    return jsonify(users), 200

def get_user(id: int) -> tuple:
    """
    Description: Handling the GET /api/v2/users/<int:id> endpoint.
    Input: Parameter id .
    Output: JSON of User object or 'message' key describing reason for process failure.
    """
    
    load_dotenv()
    db = Database()
    table_name = 'user'

    try:
        users_list = db.read(table_name, criteria={'id': id})
        
        if users_list:
            usr = users_list[0]
            user = User(*usr).toJSON()
            return jsonify(user), 200
        else:
            return jsonify({"message": "User not found."}), 404
            
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

def post_user() -> tuple:
    """
    Description: Handling the POST /api/v2/users endpoint.
    Input: JSON with 'email_address' key.
    Output: JSON of User object or 'message' key describing reason for process failure.
    """
    
    load_dotenv()
    db = Database()
    table_name = 'user'

    data = request.json

    try:
        if 'email_address' in data and 'type' in data:
                user_dict = {
                    'email_address': data['email_address'],
                    'type': data['type']
                }
                if db.insert(table_name, user_dict):
                    user_data = dict(User(*db.read(table_name, user_dict)[0]).toJSON())
                    user_data.update({"message": "User inserted successfully!"})
                    return jsonify(user_data), 200
                else:
                    return jsonify({"message": "User insertion failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key 'email_address'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
     
def auth() -> tuple:
    """
    Description: Handling the POST /api/v2/users endpoint.
    Input: JSON with 'email_address' key.
    Output: JSON of User object or 'message' key describing reason for process failure.
    """
    
    load_dotenv()
    db = Database()
    table_name = 'user'

    data = request.json
    user = None

    try:
        if 'email_address' in data:
            usr_list = db.read(table_name, criteria={'email_address': data['email_address']})
            if usr_list:
                usr = usr_list[0]
                user = User(*usr).toJSON()
            elif db.insert(table_name, {'email_address': data['email_address']}):
                usr = db.read(table_name, {'email_address': data['email_address']})[0]
                user = User(*usr).toJSON()
            else:
                return jsonify({"message": "User insert failed!"}), 501
        
            return jsonify(user), 200
        else:    
            return jsonify({"message": "Missing key 'email_address'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

def put_user() -> str:
    """
    Description: Handling the PUT /api/v2/users endpoint.
    Input: JSON with ('id', 'email_address', 'type').
    Output: JSON of User object with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database()
    table_name = 'user'

    data = request.json
    try:
        if all(key in data for key in ['id', 'email_address', 'type']):
            user_dict = {
                'id': data['id'],
                'email_address': data['email_address'],
                'type': data['type']
            }
            if db.update(table_name, user_dict, {'id': user_dict['id']}):
                user_data = dict(User(*db.read(table_name, user_dict)[0]).toJSON())
                user_data.update({"message": "User updated successfully!"})
                return jsonify(user_data), 200
            else:
                return jsonify({"message": "User update failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'email_address', 'type'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

def delete_user() -> str:
    """
    Description: Handling the DELETE /api/v2/users endpoint.
    Input: JSON with ('id', 'email_address', 'type').
    Output: JSON of User object with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database()
    table_name = 'user'

    data = request.json
    try:
        if all(key in data for key in ['id', 'email_address', 'type']):
            user_dict = {
                'id': data['id'],
                'email_address': data['email_address'],
                'type': data['type']
            }
            if db.delete(table_name, {'id': user_dict['id']}):
                user_data = dict()
                user_data.update(user_dict)
                user_data.update({"message": "User deleted successfully!"})
                return jsonify(user_data), 200
            else:
                return jsonify({"message": "User delete failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'email_address', 'type'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500







def google_auth() -> tuple:
    """
    Description: Handling the POST /api/v2/users/google_auth endpoint.
    Input: JSON with 'step' key.
    Output: JSON of User object or 'message' key describing reason for process failure.
    """
    
    db = Database()
    table_name = 'user'

    # OAuth2 Configuration
    CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
    AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URL = 'https://oauth2.googleapis.com/token'
    USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


    data = dict(request.json)
    if 'step' not in data:
        return jsonify({"message": "Missing key 'step'!"}), 400



    step = data['step']

    if step == 1:
        # Step 1: Redirect to Google OAuth2 authorization URL
        authorization_url = f"{AUTHORIZATION_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=email profile&access_type=offline&prompt=consent"
        return jsonify({"authorization_url": authorization_url}), 200

    elif step == 2:
        # Step 2: Exchange authorization code for access token
        authorization_code = data.get('code')
        if not authorization_code:
            return jsonify({"message": "Missing authorization code!"}), 400

        token_response = requests.post(TOKEN_URL, data={
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })

        if token_response.status_code != 200:
            return jsonify({"message": "Failed to obtain access token.", "error": token_response.json()}), 400

        token_data = token_response.json()
        access_token = token_data['access_token']

        # Step 3: Use the access token to get user info
        user_info_response = requests.get(USER_INFO_URL, headers={
            'Authorization': f'Bearer {access_token}'
        })

        if user_info_response.status_code != 200:
            return jsonify({"message": "Failed to fetch user info.", "error": user_info_response.json()}), 400

        user_info = dict(user_info_response.json())
        email = user_info.get('email')

        if email:
            usr_list = db.read(table_name, criteria={'email_address': data['email_address']})
            if usr_list:
                usr = usr_list[0]
                user = User(*usr).toJSON()
            elif db.insert(table_name, {'email_address': data['email_address']}):
                usr = db.read(table_name, {'email_address': data['email_address']})[0]
                user = User(*usr).toJSON()
            else:
                return jsonify({"message": "User insertion failed!"}), 501
        
            return jsonify(user), 200
        else:    
            return jsonify({"message": "Missing key 'email_address'"}), 400

    else:
        return jsonify({"message": "Invalid step!"}), 400
    