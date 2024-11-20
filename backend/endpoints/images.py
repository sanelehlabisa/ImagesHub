from flask import request, jsonify, send_from_directory, abort # type: ignore
from classes.image import Image as Im
from classes.database import Database
import os
import random
from dotenv import load_dotenv
from PIL import Image # type: ignore
from shutil import copyfile


SERVER_DIRECTORY = os.getenv('SERVER_DIRECTORY')

def recommend(images, num_of_images: int = 3) -> list[tuple[int, str, str]]:
    """
    Description: Using random packeage to recommend images.
    Input:  Integer num_of_image for number of output images.
    Output: List of Image tupple.
    """
    unique_random_image_indexes: list[int] = []
    recommended_images_list: list[tuple[int, str, str]] = []
    while len(unique_random_image_indexes) != num_of_images and len(unique_random_image_indexes) < len(images):
        random_index = random.randint(0, len(images) - 1)
        if random_index not in unique_random_image_indexes:
            unique_random_image_indexes.append(random_index)

    for index in unique_random_image_indexes:
        recommended_images_list.append(Image(*images[index]))
    return recommended_images_list

def get_images() -> tuple:
    """
    Description: Handling the GET /api/v2/images endpoint.
    Input: Query parameters ('min_id', 'max_id', 'limit', or 'model'), or nothing.
    Output: JSON of list of Image objects or 'message' key describing reason for process failure.
    """

    load_dotenv()
    db = Database()   
    table_name = 'image'

    # Get query parameters
    min_id = request.args.get('min_id', type=int)
    max_id = request.args.get('max_id', type=int)
    limit = request.args.get('limit', type=int)
    model = request.args.get('model', type=int)


    try:
        images = None
        if min_id is not None and max_id is not None:
            images = db.read_range(table_name, min_id, max_id)
        elif limit is not None:
            images = db.read(table_name, limit=limit)
        elif model is not None:
            images = db.read(table_name)
            images = recommend(images, len(images))
        else:
            images = db.read(table_name)
        
        imgs = [Im(*image).toJSON() for image in images]
        
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
    db = Database()
    table_name = 'image'

    try:
        images_list = db.read(table_name, criteria={'id': id})
        
        if images_list:
            img = images_list[0]
            image = Im(*img).toJSON()
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
    db = Database()
    table_name = 'image' 

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
    db = Database()
    table_name = 'image'

    data = request.json

    try:
        if 'img_path' not in data.keys():
            return jsonify({"message": "Missing required fields: 'img_path'"}), 400
        img_path = data['img_path']

        metadata = '{}'
        if 'metadata' in data.keys():
            metadata = data['metadata']

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
        image_dict = {
            'high_res_img_fname': high_res_img_fname,
            'low_res_img_fname': low_res_img_fname,
            'metadata': metadata
        }
        if not db.insert(table_name, image_dict):
            return jsonify({"message": "Image failed to insert."}), 401
        
        image_data = dict(Im(*db.read(table_name, image_dict)[0]).toJSON())
        image_data.update({"message": "Image successfully inserted."})
        return jsonify(image_data), 200
    
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

def put_image() -> str:
    """
    Description: Handling the PUT /api/v2/images endpoint.
    Input: JSON with ('id', 'low_res_img_fname', 'high_res_img_fname', 'metadata').
    Output: JSON of Image object with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database()
    table_name = 'image'

    data = request.json
    try:
        if all(key in data for key in ['id', 'low_res_img_fname', 'high_res_img_fname', 'metadata']):
            image_dict = {
                'id': data['id'],
                'low_res_img_fname': data['low_res_img_fname'],
                'high_res_img_fname': data['high_res_img_fname'],
                'metadata': data['metadata']
            }
            if db.update(table_name, image_dict,{'id': image_dict['id']}):
                image_data = dict(Im(*db.read(table_name, image_dict)[0]).toJSON())
                image_data.update({"message": "Image updated successfully!"})
                return jsonify(image_data), 200
            else:
                return jsonify({"message": "Image update failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'low_res_img_fname', 'high_res_img_fname', 'metadata'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

def delete_image() -> str:
    """
    Description: Handling the DELETE /api/v2/images endpoint.
    Input: JSON with ('id', 'low_res_img_fname', 'high_res_img_fname', 'metadata').
    Output: JSON of Image object with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database()
    table_name = 'image'

    data = request.json
    
    try:
        if all(key in data for key in ['id', 'low_res_img_fname', 'high_res_img_fname', 'metadata']):
            image_dict = {
                'id': data['id'],
                'low_res_img_fname': data['low_res_img_fname'],
                'high_res_img_fname': data['high_res_img_fname'],
                'metadata': data['metadata']
            }
            if db.delete(table_name, image_dict):
                image_data = dict()
                image_data.update(image_dict)
                image_data.update({"message": "Image deleted successfully!"})
                return jsonify(image_data), 200
            else:
                return jsonify({"message": "Image deleted failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'low_res_img_fname', 'high_res_img_fname', 'metadata'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500