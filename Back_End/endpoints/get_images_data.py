from bottle import response # type: ignore
import json

def get_images_data(db):
    db.set_table_name('image')
    images = db.read()

    if not images:
        response.status = 404
        return {'error': 'no images found'}

    response.status = 200
    imgs = list()
    for image in images:
        imgs.append({
            'id': image[0],
            'low_res_img_fname': image[1],
            'hig_res_img_url': image[2]
        })
    return json.dumps(imgs)
