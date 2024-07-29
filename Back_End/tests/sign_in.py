import requests # type: ignore
import json
import os

GREEN_TICK = '\033[92m✔\033[0m'  # red color tick
RED_CROSS = '\033[91m✖\033[0m'  # red cross

def test_sign_in(n):
    url = "http://localhost:8080/api/sign-in"

    payload = {
        "email_address": "test@sarao.ac.za.com" 
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()

    # Assert successful response and matching email
    try:
        assert response.status_code == 200
        assert response_data['email_address'] == payload['email_address']
        print(f"{GREEN_TICK} Test {n} passed!") 
    except AssertionError:
        print(f"{RED_CROSS} Test {n} failed!")

