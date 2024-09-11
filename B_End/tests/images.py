import requests  # type: ignore
import json
from dotenv import load_dotenv, set_key
import os

def test_get_images(params={}) -> bool:
    url = "http://localhost:5000/api/v2/images"  

    load_dotenv()
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    # Send GET images request with optional parameters
    response = requests.get(url, headers=headers, data=json.dumps(params))

    response_data = response.json()

    try:
        assert response.status_code == 200
        assert isinstance(response_data, list)
        for img_data in response_data:
            img = dict(img_data)
            assert 'id' in img.keys()
            assert 'low_res_img_fname' in img.keys()
            assert 'high_res_img_fname' in img.keys()
        return True
    except AssertionError:
        print(response_data)
        return False
    
def test_get_image(params={}) -> bool:
    url = f"http://localhost:5000/api/v2/images/{params['id']}"  

    load_dotenv()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    # Send GET images request with optional parameters
    response = requests.get(url, headers=headers, data=json.dumps(params))

    response_data = response.json()

    try:
        assert response.status_code == 200
        assert isinstance(response_data, dict)
        img = dict(response_data)
        assert 'id' in img.keys()
        assert 'low_res_img_fname' in img.keys()
        assert 'high_res_img_fname' in img.keys()
        return True
    except AssertionError:
        print(response_data)
        return False

def test_serve_image(params={}) -> bool:
    url = f"http://localhost:5000/api/v2/images/{params['filename']}"  

    load_dotenv()
    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    # Send GET images request without data
    response = requests.get(url, headers=headers)

    try:
        assert response.status_code == 200
        assert 'image' in response.headers['Content-Type']  # Check if the content type is an image
        return True
    except AssertionError:
        print(response.json())  # Print error message from the response
        return False

def test_post_image(params={}) -> bool:
    url = f"http://localhost:5000/api/v2/images"  

    load_dotenv()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    # Send POST images request with optional parameters
    response = requests.post(url, headers=headers, data=json.dumps(params))

    response_data = response.json()

    try:
        assert response.status_code == 200
        assert isinstance(response_data, dict)
        res = dict(response_data)
        assert 'message' in res.keys()
        assert res['message'] == 'Image successfully inserted.'
        return True
    except AssertionError:
        print(response_data)
        return False


if __name__ == "__main__":
    GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
    RED_CROSS = '\033[91m✖\033[0m'  # red color cross


    set_key('.env', 'DATABASE_NAME', "t_images_hub.db")


    img_path = "./res/DEEP2heat_cropped.jpg"
    if test_post_image({"img_path": img_path}):
        print(f"Post Image Test {GREEN_TICK} passed!")
    else:
        print(f"Post Image Test {RED_CROSS} failed!")

    filename = "low_res_DEEP2heat_cropped.jpg"
    if test_serve_image({"filename": filename}):
        print(f"Serve Image (filename={filename}) Test {GREEN_TICK} passed!")
    else:
        print(f"Serve Image (filename={filename}) Test {RED_CROSS} failed!")


    if test_get_images():
        print(f"Get all Images Test {GREEN_TICK} passed!")
    else:
        print(f"Get all Images Test {RED_CROSS} failed!")

    limit = 5
    if test_get_images({"limit": limit}):
        print(f"Get Images (limit={limit}) Test {GREEN_TICK} passed!")
    else:
        print(f"Get Images (limit={limit}) Test {RED_CROSS} failed!")

    min_id, max_id = 1, 10
    if test_get_images({"min_id": min_id, "max_id": max_id}):
        print(f"Get Images (min_id={min_id} & max_id={max_id}) Test {GREEN_TICK} passed!")
    else:
        print(f"Get Images (min_id={min_id} & max_id={max_id}) Test {RED_CROSS} failed!")


    id = 1
    if test_get_image({"id": id}):
        print(f"Get Image (id=1) Test {GREEN_TICK} passed!")
    else:
        print(f"Get Image (id=1) Test {RED_CROSS} failed!")


    
    set_key('.env', 'DATABASE_NAME', "images_hub.db")