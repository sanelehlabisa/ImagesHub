import requests # type: ignore
import json
import os

GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
RED_CROSS = '\033[91m✖\033[0m'  # red color cross

def test_post_request_data(n):
    url = "http://localhost:8080/api/post-request-data"
    return
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    payload = {
        "guest_id": 1,
        "img_id": 3,
        "reason": "test reason..",
        "status": 0
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()

    try:
        assert response.status_code == 200
        assert 'message' in response_data
        assert response_data['message'] == 'db insert request cmd executed successfully'
        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError:
        print(f"{RED_CROSS} Test {n} failed!")
        print(response_data)

