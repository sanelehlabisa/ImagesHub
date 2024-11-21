from flask import request, jsonify # type: ignore
from classes.request import Request
from classes.database import Database
import os
from dotenv import load_dotenv



def get_requests() -> tuple:
    """
    Description: Handling the GET /api/v2/requests endpoint.
    Input: Query parameters ('min_id', 'max_id', or 'limit'), or nothing.
    Output: JSON of list of Request objects or 'message' key describing reason for process failure.
    """

    load_dotenv()
    db = Database()
    table_name = 'request'

    # Get query parameters
    min_id = request.args.get('min_id', type=int)
    max_id = request.args.get('max_id', type=int)
    limit = request.args.get('limit', type=int)

    try:
        requests = None
        if min_id is not None and max_id is not None:
            requests = db.read_range(table_name, min_id, max_id)
        elif limit is not None:
            requests = db.read(table_name, limit=limit)
        else:
            requests = db.read(table_name)
        
        reqs = [Request(*req).toJSON() for req in requests]

        return jsonify(reqs), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    

def get_request(id: int) -> tuple:
    """
    Description: Handling the GET /api/v2/requests<int:id> endpoint.
    Input: Parameter id.
    Output: JSON of Request objects or 'message' key describing reason for process failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'request'

    try:
        requests_list = db.read(table_name, criteria={'id': id})
        
        if requests_list:
            rq = requests_list[0]
            req = Request(*rq).toJSON()
            return jsonify(req), 200
        else:
            return jsonify({"message": "Request not found."}), 404
            
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


def post_request() -> tuple:
    """
    Description: Handling the POST /api/v2/requests endpoint.
    Input: JSON with ('id', 'user_id', 'image_id', 'reason', 'status').
    Output: JSON with 'message' key indicating success or failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'request'

    data = request.json
    try:
        if all(key in data for key in ['user_id', 'image_id', 'reason', 'status']):
            request_dict = {
                'user_id': data['user_id'],
                'image_id': data['image_id'],
                'reason': data['reason'],
                'status': data['status']
            }
            if db.insert(table_name, request_dict):
                request_data = dict(Request(*db.read(table_name, request_dict)[0]).toJSON())
                request_data.update({"message": "Request inserted successfully!"})
                return jsonify(request_data), 200
            else:
                return jsonify({"message": "Request insertion failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'user_id', 'image_id', 'reason', 'status'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def put_request() -> tuple:
    """
    Description: Handling the PUT /api/v2/requests endpoint.
    Input: JSON with ('id', 'user_id', 'img_id', 'reason', 'status').
    Output: JSON with 'message' key indicating success or failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'request'

    data = request.json
    try:
        if all(key in data for key in ['id', 'user_id', 'image_id', 'reason', 'status']):
            request_dict = {
                'id': data['id'],
                'user_id': data['user_id'],
                'image_id': data['image_id'],
                'reason': data['reason'],
                'status': data['status']
            }
            if db.update(table_name, request_dict,{'id': request_dict['id']}):
                request_data = dict(Request(*db.read(table_name, request_dict)[0]).toJSON())
                request_data.update({"message": "Request updated successfully!"})
                return jsonify(request_data), 200
            else:
                return jsonify({"message": "Request update failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'user_id', 'image_id', 'reason', 'status'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def delete_request() -> tuple:
    """
    Description: Handling the DELETE /api/v2/requests endpoint.
    Input: JSON with ('id', 'user_id', 'image_id', 'reason', 'status').
    Output: JSON of Request object with 'message' key indicating success or failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'request'

    data = request.json
    try:
        if all(key in data for key in ['id', 'user_id', 'image_id', 'reason', 'status']):
            request_dict = {
                'id': data['id'],
                'user_id': data['user_id'],
                'image_id': data['image_id'],
                'reason': data['reason'],
                'status': data['status']
            }
            if db.delete(table_name, {'id': request_dict['id']}):
                request_data = dict()
                request_data.update(request_dict)
                request_data.update({"message": "Request deleted successfully!"})
                return jsonify(request_data), 200
            else:
                return jsonify({"message": "Request delete failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'user_id', 'image_id', 'reason', 'status'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500