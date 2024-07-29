from bottle import request, response # type: ignore
from PIL import Image # type: ignore
from shutil import copyfile
import os
from urllib.parse import urlparse, urljoin

HOST = "localhost"
PORT = 8080
SERVER_DIRECTORY = "server"

def post_image_data(db):
    try:
        img_path = request.json.get('img_path', None)
        
        if img_path is None: 
            response.status = 400
            return {'error': 'image path parameter is required'}
        elif not os.path.isfile(img_path):
            response.status = 401
            return {'error': 'invalid image path'}

        with Image.open(img_path) as img:
            low_res_img = img.resize((100, int(img.height * 100.0 / img.width)), Image.BICUBIC)
        
        filename = os.path.basename(img_path)
        low_res_destination_path = os.path.join(SERVER_DIRECTORY, "low_res_" + filename)
        low_res_img.save(low_res_destination_path)
        
        high_res_destination_path = os.path.join(SERVER_DIRECTORY, "high_res_" + filename)
        copyfile(img_path, high_res_destination_path)
        
        BASE_URL = f'http://{HOST}:{PORT}/api/serve-image/'
        high_res_img_fname =urljoin(BASE_URL, f"high_res_{filename}")
        low_res_img_fname = urljoin(BASE_URL, f"low_res_{filename}")
        
        db.set_table_name('image')
        if not db.insert(
            {
                'high_res_img_fname': high_res_img_fname,
                'low_res_img_fname': low_res_img_fname
            }):
            response.status = 500
            return {"error": "db img insert cmd failed to execute"}
        
        response.status = 200
        return {'message': 'db insert image cmd executed successfully'}
    
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

