import requests
import json
import os

GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
RED_CROSS = '\033[91m✖\033[0m'  # red color cross

def test_post_image_data(n):
    url = "http://localhost:8080/api/post-image-data"
    return
    img_path = "./res/n1316compositeGREENmasked.png"
    
    #"radio bubbles.jpg",
    #"Xgalaxy_composite.jpg"

    # Check if the file exists
    if not os.path.exists(img_path):
        print(f"{RED_CROSS} Test {n} failed!")
        print(f"Error: '{img_path}' does not exist.")
        return

    payload = {
        "img_path": img_path
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()

    # Assert successful response and expected output
    try:
        assert response.status_code == 200
        assert 'message' in response_data and response_data['message'] == 'db insert image cmd executed successfully'
        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError:
        print(f"{RED_CROSS} Test {n} failed!")
        print(response_data)
