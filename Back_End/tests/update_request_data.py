import requests # type: ignore
import json
import os

GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
RED_CROSS = '\033[91m✖\033[0m'  # red color cross

def test_update_request_data(n):
    url = "http://localhost:8080/api/update-request-data"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    # Test PUT request with valid data
    request_data = {
        "id": 1,
        "guest_id": 1,
        "status": 1
    }
    response = requests.put(url, headers=headers, json=request_data)
    response_data = response.json()

    try:
        assert response.status_code == 200
        assert 'message' in response_data
        assert response_data['message'] == 'db update request cmd executed successfully'
        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError:
        print(f"{RED_CROSS} Test {n} failed!")
        print(response_data)
