from flask import request, jsonify # type: ignore
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
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('guest')
    users = []

    # Get query parameters
    min_id = request.args.get('min_id', type=int)
    max_id = request.args.get('max_id', type=int)
    limit = request.args.get('limit', type=int)

    for i, table_name in enumerate(['guest', 'administrator']):
        db.set_table_name(table_name)
        try:
            if min_id is not None and max_id is not None:
                for user in db.read_range(min_id, max_id):
                    users.append(User(user[0], user[1], i).toJSON())
            elif limit is not None:
                for user in db.read(limit=limit):
                    users.append(User(user[0], user[1], i).toJSON())
            else:
                for user in db.read():
                    users.append(User(user[0], user[1], i).toJSON())
            
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
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('guest')

    try:
        users_list = db.read(criteria={'id': id})
        
        if users_list:
            usr = users_list[0]
            user = User(usr[0], usr[1], 0).toJSON()
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
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('guest')

    data = request.json

    try:
        if 'email_address' in data:
                if db.insert({'email_address': data['email_address']}):
                    return jsonify({"message": "User inserted successfully!"}), 200
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
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('guest')

    data = request.json
    user = None

    try:
        if 'email_address' in data:
            for i, table_name in enumerate(['guest', 'administrator']):
                db.set_table_name(table_name)
                usr_list = db.read(criteria={'email_address': data['email_address']})
                if usr_list:
                    usr = usr_list[0]
                    user = User(int(usr[0]), str(usr[1]), i).toJSON()
            
            if not user:
                db.set_table_name('guest')
                if db.insert({'email_address': data['email_address']}):
                    usr = db.read({'email_address': data['email_address']})[0]
                    user = User(int(usr[0]), str(usr[1]), 0).toJSON()
                else:
                    return jsonify({"message": "User insertion failed!"}), 501
            
            return jsonify(user), 200
        
        else:    
            return jsonify({"message": "Missing key 'email_address'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500