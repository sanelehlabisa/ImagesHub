from flask import request, jsonify, send_from_directory, abort # type: ignore
from classes.image import Image as Im
from classes.database import Database
import os
from dotenv import load_dotenv
from PIL import Image # type: ignore
from shutil import copyfile


SERVER_DIRECTORY = os.getenv('SERVER_DIRECTORY')

def get_images() -> tuple:
    """
    Description: Handling the GET /api/v2/images endpoint.
    Input: Query parameters ('min_id', 'max_id', or 'limit'), or nothing.
    Output: JSON of list of Image objects or 'message' key describing reason for process failure.
    """

    load_dotenv()
    db = Database(os.getenv('DATABASE_NAME'))
    db.set_table_name('image')    

    # Get query parameters
    min_id = request.args.get('min_id', type=int)
    max_id = request.args.get('max_id', type=int)
    limit = request.args.get('limit', type=int)

    try:
        images = None
        if min_id is not None and max_id is not None:
            images = db.read_range(min_id, max_id)
        elif limit is not None:
            images = db.read(limit=limit)
        else:
            images = db.read()
        
        imgs = [Im(image[0], image[1], image[2]).toJSON() for image in images]

        return jsonify(imgs), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


def get_image(id) -> tuple:
    """
    Description: Handling the GET /api/v2/images<int:id> endpoint.
    Input: Parameter id.
    Output: JSON of Image object or 'message' key describing reason for process failure.
    """

    load_dotenv()
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('image')  

    try:
        images_list = db.read(criteria={'id': id})
        
        if images_list:
            img = images_list[0]
            image = Im(img[0], img[1], img[2]).toJSON()
            return jsonify(image), 200
        else:
            return jsonify({"message": "Image not found."}), 404
            
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

def serve_image(filename) -> tuple:
    """
    Description: Handling the GET /api/v2/images/<string:filename> endpoint.
    Input: Parameter filename.
    Output: Serves the image file directly.
    """

    load_dotenv()
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('image')  

    try:
        return send_from_directory(SERVER_DIRECTORY, filename)
    except FileNotFoundError:
        abort(404)  # Return a 404 error if the file is not found
    


def post_image() -> tuple:
    """
    Description: Handling the POST /api/v2/images endpoint.
    Input: JSON with 'img_path'.
    Output: JSON with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database(os.getenv('DATABASE_NAME'))
    
    db.set_table_name('image')  

    data = request.json

    try:
        if 'img_path' not in data.keys():
            return jsonify({"message": "Missing required fields: 'img_path'"}), 400
        img_path = data['img_path']

        print(f"img_path: {img_path}")
        print(f"SERVER_DIRECTORY: {SERVER_DIRECTORY}")

        if not os.path.isfile(img_path):
            return jsonify({"message": "Invalid image path"}), 401

        with Image.open(img_path) as img:
            low_res_img = img.resize((100, int(img.height * 100.0 / img.width)), Image.BICUBIC)
        
        filename = os.path.basename(img_path)
        low_res_destination_path = os.path.join(SERVER_DIRECTORY, "low_res_" + filename)
        low_res_img.save(low_res_destination_path)
        
        high_res_destination_path = os.path.join(SERVER_DIRECTORY, "high_res_" + filename)
        copyfile(img_path, high_res_destination_path)
        
       
        high_res_img_fname = f"high_res_{filename}"
        low_res_img_fname = f"low_res_{filename}"
        
        db.set_table_name('image')
        if not db.insert(
            {
                'high_res_img_fname': high_res_img_fname,
                'low_res_img_fname': low_res_img_fname
            }):
            return jsonify({"message": "Image failed to insert."}), 401
        
        return jsonify({"message": "Image successfully inserted."}), 200
    
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
