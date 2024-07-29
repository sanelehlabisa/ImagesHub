import requests # type: ignore
import json
import os

GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
RED_CROSS = '\033[91m✖\033[0m'  # red color cross

def test_get_requests_data(n):
    url = "http://localhost:8080/api/get-requests-data"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    # Test GET request
    response = requests.get(url, headers=headers)
    response_data = response.json()

    try:
        assert response.status_code == 200
        assert isinstance(response_data, list)
        for request in response_data:
            req = dict(request)
            assert 'id' in req
            assert 'guest_id' in req
            assert 'img_id' in req
            assert 'reason' in req
            assert 'status' in req
        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError:
        print(f"{RED_CROSS} Test {n} failed!")
        print(response_data)

