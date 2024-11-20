import requests  # type: ignore
import json
from dotenv import load_dotenv, set_key
import os

load_dotenv()

def make_request(method: str, url: str, params: dict = None) -> dict:
    load_dotenv()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }
    
    if method == 'GET':
        response = requests.get(url, headers=headers, data=json.dumps(params))
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=json.dumps(params))
    else:
        raise ValueError("Unsupported HTTP method")
 
    return response

def assert_response(response, expected_type: str, keys: list) -> bool:
    response_data = response.json()
    try:
        assert response.status_code == 200
        assert isinstance(response_data, expected_type)
        return True
    except AssertionError:
        print(response_data)
        return False

def test_api(endpoint: str, method: str, params: dict, expected_type: str, keys: list) -> bool:
    url = f"http://localhost:5000/api/v2{endpoint}"
    response = make_request(method, url, params)
    return assert_response(response, expected_type, keys)

def run_tests():
    GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
    RED_CROSS = '\033[91m✖\033[0m'  # red color cross

    set_key('.env', 'DATABASE_NAME', "t_images_hub.db")

    # Test POST user
    email_address = "smazibuko@dut.ac.za"
    if test_api("/users", "POST", {"email_address": email_address}, dict, ["message"]):
        print(f"Post User ('email_address'={email_address}) Test {GREEN_TICK} passed!")
    else:
        print(f"Post User ('email_address'={email_address}) Test {RED_CROSS} failed!")

    # Test Auth user
    email_address = "shlabisa@ukzn.ac.za"
    if test_api("/auth", "POST", {"email_address": email_address}, dict, ["id", "email_address", "type"]):
        print(f"Auth User ('email_address'={email_address}) Test {GREEN_TICK} passed!")
    else:
        print(f"Auth User ('email_address'={email_address}) Test {RED_CROSS} failed!")

    # Test Get all users
    if test_api("/users", "GET", {}, list, ["id", "email_address", "type"]):
        print(f"Get all Users Test {GREEN_TICK} passed!")
    else:
        print(f"Get all Users Test {RED_CROSS} failed!")

    # Test Get users with limit
    limit = 5
    if test_api("/users", "GET", {"limit": limit}, list, ["id", "email_address", "type"]):
        print(f"Get Users (limit={limit}) Test {GREEN_TICK} passed!")
    else:
        print(f"Get User (limit={limit}) Test {RED_CROSS} failed!")

    # Test Get users with min_id and max_id
    min_id, max_id = 1, 10
    if test_api("/users", "GET", {"min_id": min_id, "max_id": max_id}, list, ["id", "email_address", "type"]):
        print(f"Get User (min_id={min_id} & max_id={max_id}) Test {GREEN_TICK} passed!")
    else:
        print(f"Get User (min_id={min_id} & max_id={max_id}) Test {RED_CROSS} failed!")

    # Test Get user by id
    id = 1
    if test_api(f"/users/{id}", "GET", {}, dict, ["id", "email_address", "type"]):
        print(f"Get User (id={id}) Test {GREEN_TICK} passed!")
    else:
        print(f"Get User (id={id}) Test {RED_CROSS} failed!")

    set_key('.env', 'DATABASE_NAME', "images_hub.db")

if __name__ == "__main__":
    run_tests()
