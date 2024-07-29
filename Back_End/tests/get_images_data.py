import requests # type: ignore
import json
import os

GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
RED_CROSS = '\033[91m✖\033[0m'  # red color cross

def test_get_images_data(n):
    url = "http://localhost:8080/api/get-images-data"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    # Assert successful response and expected output
    try:
        assert response.status_code == 200
        assert isinstance(response_data, list)
        for img_data in response_data:
            img = dict(img_data)
            assert 'id' in img.keys()
            assert 'low_res_img_fname' in img.keys()
            assert 'hig_res_img_url' in img.keys()
        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError:
        print(f"{RED_CROSS} Test {n} failed!")
        print(response_data)
