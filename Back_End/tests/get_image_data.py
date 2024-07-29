import requests # type: ignore
import json
import os

GREEN_TICK = '\033[92m✔\033[0m'
RED_CROSS = '\033[91m✖\033[0m'

def test_get_image_data(n):
    url = "http://localhost:8080/api/get-image-data/2"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    try:
        assert response.status_code == 200
        assert isinstance(response_data, dict)
        assert 'id' in response_data
        assert 'high_res_img_fname' in response_data
        assert 'low_res_img_fname' in response_data
        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError:
        print(f"{RED_CROSS} Test {n} failed!")
        print(response_data)
