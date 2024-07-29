import requests # type: ignore
import json
import os

GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
RED_CROSS = '\033[91m✖\033[0m'  # red color cross

def test_get_request_data(n: int, request_id: int=1):
    base_url = "http://localhost:8080"
    get_user_url = f"{base_url}/api/get-request-data/{request_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    # Test GET request
    response = requests.get(get_user_url, headers=headers)
    req_data = response.json()

    try:
        assert response.status_code == 200
        assert isinstance(req_data, dict)
        assert 'id' in req_data
        assert 'guest_id' in req_data
        assert 'img_id' in req_data
        assert 'reason' in req_data
        assert 'status' in req_data
        assert req_data['id'] == request_id

        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError as e:
        print(f"{RED_CROSS} Test {n} failed: {e}")
        print(req_data)
