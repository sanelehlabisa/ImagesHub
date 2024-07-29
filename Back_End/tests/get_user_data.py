import requests # type: ignore
import json
import os

GREEN_TICK = '\033[92m✔\033[0m'
RED_CROSS = '\033[91m✖\033[0m'


def test_get_user_data(n: int, user_id: int=1):
    base_url = "http://localhost:8080"
    get_user_url = f"{base_url}/api/get-user-data/{user_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    response = requests.get(get_user_url, headers=headers)

    try:
        assert response.status_code == 200
        user_data = response.json()

        assert 'id' in user_data
        assert 'email_address' in user_data
        assert 'type' in user_data
        assert user_data['id'] == user_id

        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError as e:
        print(f"{RED_CROSS} Test {n} failed: {e}")
        print(response.text)
