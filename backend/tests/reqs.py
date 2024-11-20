import requests # type: ignore
import json
from dotenv import load_dotenv, set_key
import os

def test_get_requests(params={}) -> bool:
    url = "http://localhost:5000/api/v2/requests"  

    load_dotenv()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    # Send GET images request with optional parameters
    response = requests.get(url, headers=headers, data=json.dumps(params))

    response_data = response.json()

    try:
        assert response.status_code == 200
        assert isinstance(response_data, list)
        for req in response_data:
            request = dict(req)
            assert 'id' in request.keys()
            assert 'image_id' in request.keys()
            assert 'user_id' in request.keys()
            assert 'reason' in request.keys()
            assert 'status' in request.keys()
        return True
    except AssertionError:
        print(response_data)
        return False

def test_get_request(params={}) -> bool:
    if 'id' in params.keys():
        url = f"http://localhost:5000/api/v2/requests/{params['id']}"
        load_dotenv()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('API_KEY')}"
        }

        # Send GET images request with optional parameters
        response = requests.get(url, headers=headers, data=json.dumps(params))

        response_data = response.json()

        try:
            assert response.status_code == 200
            assert isinstance(response_data, dict)
            req_json = response_data
            req = dict(req_json)
            assert 'id' in req.keys()
            assert 'user_id' in req.keys()
            assert 'image_id' in req.keys()
            assert 'reason' in req.keys()
            assert 'status' in req.keys()
            return True
        except AssertionError:
            print(response_data)
    
    return False

def test_post_request(params={}) -> bool:
    if all(key in params for key in ['user_id', 'image_id', 'reason', 'status']):
        url = f"http://localhost:5000/api/v2/requests"
        load_dotenv()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('API_KEY')}"
        }

        # Send POST images request with optional parameters
        response = requests.post(url, headers=headers, data=json.dumps(params))

        response_data = response.json()

        try:
            assert response.status_code == 200
            assert isinstance(response_data, dict)
            res_json = response_data
            res = dict(res_json)
            assert 'message' in res.keys()
            return True
        except AssertionError:
            print(response_data)
    
    return False

def test_put_request(params={}):
    if all(key in params for key in ['id', 'user_id', 'image_id', 'reason', 'status']):
        url = f"http://localhost:5000/api/v2/requests"
        load_dotenv()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('API_KEY')}"
        }

        # Send PUT images request with optional parameters
        response = requests.put(url, headers=headers, data=json.dumps(params))

        response_data = response.json()

        try:
            assert response.status_code == 200
            assert isinstance(response_data, dict)
            res_json = response_data
            res = dict(res_json)
            assert 'message' in res.keys()
            assert 'Request updated successfully!' in res['message']
            return True
        except AssertionError:
            print(response_data)
    
    return False

if __name__ == "__main__":
    GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
    RED_CROSS = '\033[91m✖\033[0m'  # red color cross

    set_key('.env', 'DATABASE_NAME', "t_images_hub.db")

    user_id, image_id, reason, status = 1, 1, "Hi This is a test request", 0
    if test_post_request({
        "user_id": user_id,
        "image_id": image_id,
        "reason": reason,
        "status": status
        }):
        print(f"Post Request (user_id=1, image_id=1, reason='Hi This is a test request', status=0) Test {GREEN_TICK} passed!")
    else:
        print(f"Post Request (user_id=1, image_id=1, reason='Hi This is a test request', status=0) Test {RED_CROSS} failed!")


    if test_get_requests():
        print(f"Get all Requests Test {GREEN_TICK} passed!")
    else:
        print(f"Get all Requests Test {RED_CROSS} failed!")

    limit = 5
    if test_get_requests({"limit": limit}):
        print(f"Get Requests (limit={limit}) Test {GREEN_TICK} passed!")
    else:
        print(f"Get Requests (limit={limit}) Test {RED_CROSS} failed!")

    min_id, max_id = 1, 10
    if test_get_requests({"min_id": min_id, "max_id": max_id}):
        print(f"Get Requests (min_id={min_id} & max_id={max_id}) Test {GREEN_TICK} passed!")
    else:
        print(f"Get Requests (min_id={min_id} & max_id={max_id}) Test {RED_CROSS} failed!")


    id = 1
    if test_get_request({"id": id}):
        print(f"Get Request (id=1) Test {GREEN_TICK} passed!")
    else:
        print(f"Get Request (id=1) Test {RED_CROSS} failed!")


    user_id, image_id, reason, status = 1, 1, "Hi This is an updated test request", 0
    if test_put_request({
        "id": id,
        "user_id": user_id,
        "image_id": image_id,
        "reason": reason,
        "status": status
        }):
        print(f"Put Request (id=1) Test {GREEN_TICK} passed!")
    else:
        print(f"Put Request (id=1) Test {RED_CROSS} failed!")


    set_key('.env', 'DATABASE_NAME', "images_hub.db")