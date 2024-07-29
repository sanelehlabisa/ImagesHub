import requests # type: ignore
import json
import os

GREEN_TICK = '\033[92m✔\033[0m'
RED_CROSS = '\033[91m✖\033[0m'


def test_get_users_data(n: int, email_address: str="test@sarao.ac.za.com"):
    base_url = "http://localhost:8080"
    get_users_url = f"{base_url}/api/get-users-data"

    response = requests.get(get_users_url)

    try:
        assert response.status_code == 200
        user_data = json.loads(response.text)

        found_user = None
        for user in user_data:
            if user['email_address'] == email_address:
                found_user = user
                break

        assert found_user is not None, f"User data for '{email_address}' not found."
        assert found_user['email_address'] == email_address
        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError as e:
        print(f"{RED_CROSS} Test {n} failed: {e}")
