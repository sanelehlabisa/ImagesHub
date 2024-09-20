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
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('request')

    # Get query parameters
    min_id = request.args.get('min_id', type=int)
    max_id = request.args.get('max_id', type=int)
    limit = request.args.get('limit', type=int)

    try:
        requests = None
        if min_id is not None and max_id is not None:
            requests = db.read_range(min_id, max_id)
        elif limit is not None:
            requests = db.read(limit=limit)
        else:
            requests = db.read()
        
        reqs = [Request(req[0], req[1], req[2], req[3], req[4]).toJSON() for req in requests]

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
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('request')

    try:
        requests_list = db.read(criteria={'id': id})
        
        if requests_list:
            rq = requests_list[0]
            req = Request(rq[0], rq[1], rq[2], rq[3], rq[4]).toJSON()
            return jsonify(req), 200
        else:
            return jsonify({"message": "Request not found."}), 404
            
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


def post_request() -> str:
    """
    Description: Handling the POST /api/v2/requests endpoint.
    Input: JSON with ('id', 'guest_id', 'image_id', 'reason', 'status').
    Output: JSON with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('request')

    data = request.json

    try:
        if all(key in data for key in ['guest_id', 'image_id', 'reason', 'status']):
                if db.insert({
                    'guest_id': data['guest_id'],
                    'image_id': data['image_id'],
                    'reason': data['reason'],
                    'status': data['status']
                    }):
                    return jsonify({"message": "Request inserted successfully!"}), 200
                else:
                    return jsonify({"message": "Request insertion failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'guest_id', 'image_id', 'reason', 'status'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def put_request() -> str:
    """
    Description: Handling the PUT /api/v2/requests endpoint.
    Input: JSON with ('id', 'guest_id', 'img_id', 'reason', 'status').
    Output: JSON with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('request')

    data = request.json

    try:
        if all(key in data for key in ['id', 'guest_id', 'image_id', 'reason', 'status']):
                if db.update({
                    'guest_id': data['guest_id'],
                    'image_id': data['image_id'],
                    'reason': data['reason'],
                    'status': data['status']
                },{
                     'id': data['id']
                }
                ):
                    return jsonify({"message": "Request updated successfully!"}), 200
                else:
                    return jsonify({"message": "Request update failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'guest_id', 'image_id', 'reason', 'status'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500