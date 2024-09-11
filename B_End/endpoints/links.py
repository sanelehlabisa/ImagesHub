from flask import request, jsonify # type: ignore
from classes.link import Link
from classes.database import Database
import os
from dotenv import load_dotenv



def get_links() -> tuple:
    """
    Description: Handling the GET /api/v2/links endpoint.
    Input: Query parameters ('min_id', 'max_id', or 'limit'), or nothing.
    Output: JSON of list of Link objects or 'message' key describing reason for process failure.
    """

    load_dotenv()
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('link')

    # Get query parameters
    min_id = request.args.get('min_id', type=int)
    max_id = request.args.get('max_id', type=int)
    limit = request.args.get('limit', type=int)

    try:
        links = None
        if min_id is not None and max_id is not None:
            links = db.read_range(min_id, max_id)
        elif limit is not None:
            links = db.read(limit=limit)
        else:
            links = db.read()
        
        lnks = [Link(lnk[0], lnk[1], lnk[2], lnk[3]).toJSON() for lnk in links]

        return jsonify(lnks), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    

def get_link(id: int) -> tuple:
    """
    Description: Handling the GET /api/v2/links<int:id> endpoint.
    Input: Parameter id.
    Output: JSON of Link objects or 'message' key describing reason for process failure.
    """

    load_dotenv()
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('link')

    try:
        links_list = db.read(criteria={'id': id})
        
        if links_list:
            link = links_list[0]
            lnk = Link(link[0], link[1], link[2], link[3]).toJSON()
            return jsonify(lnk), 200
        else:
            return jsonify({"message": "Link not found."}), 404
            
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

def post_link() -> tuple:
    """
    Description: Handling the POST /api/v2/links endpoint.
    Input: JSON with ('id', 'image_id', 'key', 'limit').
    Output: JSON of Link object with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database(os.getenv('DATABASE_NAME'))
    if not db.clear():
        exit()
    db.set_table_name('link')

    data = request.json

    try:
        if all(key in data for key in ['image_id', 'key', 'limit']):
                if db.insert({
                    'image_id': data['image_id'],
                    'key': data['key'],
                    'key': data['limit']
                    }):
                    return jsonify({"message": "Link inserted successfully!"}), 200
                else:
                    return jsonify({"message": "Link insertion failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'image_id', 'key', 'limit'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def put_link() -> str:
    """
    Description: Handling the PUT /api/v2/links endpoint.
    Input: JSON with ('id', 'image_id', 'key', 'limit').
    Output: JSON with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('link')

    data = request.json

    try:
        if all(key in data for key in ['id', 'image_id', 'key', 'limit']):
                if db.update({
                    'image_id': data['image_id'],
                    'key': data['key'],
                    'limit': data['limit']
                },{
                     'id': data['id']
                }
                ):
                    return jsonify({"message": "Link updated successfully!"}), 200
                else:
                    return jsonify({"message": "Link update failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'image_id', 'key', 'limit'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500