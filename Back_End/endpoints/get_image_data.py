from bottle import response # type: ignore
import json
from classes import Image_Data 

def get_image_data(db, id):
    db.set_table_name('image')
    image_data = db.read({'id': id})

    if not image_data:
        response.status = 404
        return {'error': 'image not found'}

    response.status = 200
    img_data = Image_Data(image_data[0][0], image_data[0][1], image_data[0][2]).__dict__

    return json.dumps(img_data)