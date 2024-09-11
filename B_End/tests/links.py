import requests  # type: ignore
import json
from dotenv import load_dotenv, set_key
import os

load_dotenv()

def make_request(method: str, url: str, params: dict = None, args=None) -> dict:
    load_dotenv()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }
    
    if method == 'GET':
        response = requests.get(url, headers=headers, data=json.dumps(params))
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=json.dumps(params))
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=json.dumps(params))
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

    # Test POST link
    image_id = 1
    key = "123 456 789 012"
    limit = 5
    print(f"Post Link ('image_id'={image_id}, 'key'={key},'limit'={limit}) Test", end="")
    if test_api("/links", "POST", {"image_id": image_id, "key": key, "limit": limit}, dict, ["message"]):
        print(f"{GREEN_TICK} passed!")
    else:
        print(f"{RED_CROSS} failed!")

    # Test Get all links
    print(f"Get all Link Test", end="") 
    if test_api("/links", "GET", {}, list, ["id", "image_id", "key", "limit"]):
        print(f"{GREEN_TICK} passed!")
    else:
        print(f"{RED_CROSS} failed!")

    # Test Get links with limit
    limit = 5
    print(f"Get Links (limit={limit}) Test", end="")
    if test_api(f"/links?limit=5", "GET", None, list, ["id", "image_id", "key", "limit"]):
        print(f"{GREEN_TICK} passed!")
    else:
        print(f"{RED_CROSS} failed!")

    # Test Get links with min_id and max_id
    min_id, max_id = 1, 10
    print(f"Get Links (min_id={min_id} & max_id={max_id}) Test", end="")
    if test_api(f"/links?=min_id={min_id}&max_id={max_id}", "GET", None, list, ["id", "image_id", "key", "limit"]):
        print("{GREEN_TICK} passed!")
    else:
        print(f"{RED_CROSS} failed!")

    # Test Get link by id
    id = 1
    print(f"Get Links (id={id}) Test ", end="")
    if test_api(f"/links/{id}", "GET", {}, dict, ["id", "image_id", "key", "limit"]):
        print(f"{GREEN_TICK} passed!")
    else:
        print(f"{RED_CROSS} failed!")

    # Test Put link
    id = 1
    image_id = 1
    key = "987 654 321 098"
    print(f"Put Links ('id'={id}, 'image_id'={image_id}, 'key'={key},'limit'={limit}) Test ", end="")
    if test_api(f"/links", "PUT", {"id": id, "image_id": image_id, "key": key, "limit": limit}, dict, ["message"]):
        print(f"{GREEN_TICK} passed!")
    else:
        print(f"{RED_CROSS} failed!")

    set_key('.env', 'DATABASE_NAME', "images_hub.db")

if __name__ == "__main__":
    run_tests()
