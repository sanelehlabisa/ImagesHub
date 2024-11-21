import os
from dotenv import load_dotenv
from flask import request, jsonify, send_from_directory, abort
from classes.link import Link
from classes.image import Image
from classes.database import Database

SERVER_DIRECTORY = os.getenv('SERVER_DIRECTORY')

def get_links() -> tuple:
    """
    Description: Handling the GET /api/v2/links endpoint.
    Input: Query parameters ('min_id', 'max_id', or 'limit'), or nothing.
    Output: JSON of list of Link objects or 'message' key describing reason for process failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'link'

    # Get query parameters
    min_id = request.args.get('min_id', type=int)
    max_id = request.args.get('max_id', type=int)
    limit = request.args.get('limit', type=int)

    try:
        links = None
        if min_id is not None and max_id is not None:
            links = db.read_range(table_name, min_id, max_id)
        elif limit is not None:
            links = db.read(table_name,limit=limit)
        else:
            links = db.read(table_name)
        
        lnks = [Link(*lnk).toJSON() for lnk in links]

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
    db = Database()
    table_name = 'link'

    try:
        links_list = db.read(table_name, criteria={'id': id})
        
        if links_list:
            link = links_list[0]
            lnk = Link(*link).toJSON()
            return jsonify(lnk), 200
        else:
            return jsonify({"message": "Link not found."}), 404
            
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


def download_image(key: str) -> tuple:
    """
    Description: Handling the GET /api/v2/links<string:key> endpoint.
    Input: Parameter key.
    Output: Download image or JSON or 'message' key describing reason for process failure.
    """
    db = Database()
    table_name = 'link'
    
    try:
        links_list = db.read(table_name, criteria={'key': key})
        
        if links_list:
            link = links_list[0]
            lnk = Link(*link)
            if lnk.limit == 0:
                return jsonify({"message": "Link is expired."}), 403
            
            images_list = db.read("image", criteria={'id': lnk.image_id})
            if images_list:
                image = images_list[0]
                img = Image(*image)
                filename = img.high_res_img_fname
                lnk.limit = lnk.limit - 1
                if db.update(table_name, {"limit": lnk.limit},{'id': lnk.id}):
                    return send_from_directory(SERVER_DIRECTORY, filename, as_attachment=True)
                else:
                    return jsonify({"message": "Link update failed."}), 404
            else:
                return jsonify({"message": "Image not found."}), 404
        else:
            return jsonify({"message": "Link not found."}), 404

    except FileNotFoundError:
        abort(404)  # Return a 404 error if the file is not found
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


def post_link() -> tuple:
    """
    Description: Handling the POST /api/v2/links endpoint.
    Input: JSON with ('id', 'image_id', 'key', 'limit').
    Output: JSON of Link object with 'message' key indicating success or failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'link'

    data = request.json
    try:
        if all(key in data for key in ['image_id', 'key', 'limit']):
            link_dict: dict = {
                'image_id': data['image_id'],
                'key': data['key'],
                'limit': data['limit']
            }
            if db.insert(table_name, link_dict):
                link_data = dict(Link(*db.read(table_name, link_dict)[0]).toJSON())
                link_data.update({"message": "Link inserted successfully!"})
                return jsonify(link_data), 200
            else:
                return jsonify({"message": "Link insertion failed!"}), 501
        else:    
            return jsonify({"message": "Missing key(s) 'image_id', 'key', 'limit'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def put_link() -> tuple:
    """
    Description: Handling the PUT /api/v2/links endpoint.
    Input: JSON with ('id', 'image_id', 'key', 'limit').
    Output: JSON with 'message' key indicating success or failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'link'

    data = request.json

    try:
        if all(key in data for key in ['id', 'image_id', 'key', 'limit']):
            link_dict = {
                'id': data['id'],
                'image_id': data['image_id'],
                'key': data['key'],
                'limit': data['limit']
            }
            if db.update(table_name, link_dict,{'id': link_dict['id']}):
                link_data = dict(Link(*db.read(table_name, link_dict)[0]).toJSON())
                link_data.update({"message": "Link updated successfully!"})
                return jsonify(link_data), 200
            else:
                return jsonify({"message": "Link update failed!"}), 501
        
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'image_id', 'key', 'limit'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def delete_link() -> tuple:
    """
    Description: Handling the DELETE /api/v2/links endpoint.
    Input: JSON with ('id', 'image_id', 'key', 'limit').
    Output: JSON of Link object with 'message' key indicating success or failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'link'

    data = request.json
    try:
        if all(key in data for key in ['id', 'image_id', 'key', 'limit']):
            link_dict = {
                'id': data['id'],
                'image_id': data['image_id'],
                'key': data['key'],
                'limit': data['limit']
            }
            if db.delete(table_name, {'id': link_dict['id']}):
                link_data = dict()
                link_data.update(link_dict)
                link_data.update({"message": "Link deleted successfully!"})
                return jsonify(link_data), 200
            else:
                return jsonify({"message": "Link delete failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'image_id', 'key', 'limit'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
