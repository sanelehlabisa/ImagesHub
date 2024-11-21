"""This file is responsible for testing the requests enpoint using pytest"""
import os
import json
from dotenv import load_dotenv
from main import app
from classes import Database

URL = "http://localhost:5000/api/v2/requests"
load_dotenv()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}"
}

def test_post_request() -> None:
    """This function tests the functionality of POST requests endpoint"""
    request_data = {
        'user_id': 1,
        'image_id': 1,
        'reason': "Test reason...",
        'status': 1
    }

    with app.test_client() as client:
        response = client.post(URL, headers=headers, json=request_data)
        request_dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(request_dict, dict)
        assert "user_id" in request_dict.keys()
        assert request_data["user_id"] == request_dict["user_id"]
        assert "image_id" in request_dict.keys()
        assert request_data["image_id"] == request_dict["image_id"]
        assert "reason" in request_dict.keys()
        assert request_data["reason"] == request_dict["reason"]
        assert "status" in request_dict.keys()
        assert request_data["status"] == request_dict["status"]

def test_get_requests() -> None:
    """This function tests the functionality of the GET requests endpoint."""
    request_data = {}

    with app.test_client() as client:
        response = client.get(URL, headers=headers, json=request_data)
        requests_list: list[dict] = response.get_json()

        assert response.status_code == 200
        assert isinstance(requests_list, list)
        for request_dict in requests_list:
            assert "id" in request_dict.keys()
            assert "user_id" in request_dict.keys()
            assert "image_id" in request_dict.keys()
            assert "reason" in request_dict.keys()
            assert "status" in request_dict.keys()

def test_put_request() -> None:
    """This function tests the functionality of the PUT requests endpoint"""
    request_data = {
        'id': 1,
        'user_id': 1,
        'image_id': 1,
        'reason': "Test reason...",
        'status': 1
    }

    with app.test_client() as client:
        response = client.put(URL, headers=headers, data=json.dumps(request_data))
        request_dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(request_dict, dict)
        assert "message" in request_dict.keys()
        assert "Request updated successfully!" in request_dict["message"]
        assert "id" in request_dict.keys()
        assert request_dict["id"] == request_dict["id"]
        assert "user_id" in request_dict.keys()
        assert request_dict["user_id"] == request_dict["user_id"]
        assert "image_id" in request_dict.keys()
        assert request_dict["image_id"] == request_dict["image_id"]
        assert "reason" in request_dict.keys()
        assert request_dict["reason"] == request_dict["reason"]
        assert "status" in request_dict.keys()
        assert request_dict["status"] == request_dict["status"]

def test_delete_request() -> None:
    """This function tests the functionality of the DELETE request endpoint"""
    request_data = {
        'id': 1,
        'user_id': 1,
        'image_id': 1,
        'reason': "Test reason...",
        'status': 1
    }

    with app.test_client() as client:
        response = client.delete(URL, headers=headers, json=request_data)
        request_dict: dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(request_dict, dict)
        assert "message" in request_dict.keys()
        assert "Request deleted successfully!" in request_dict["message"]
        assert "id" in request_dict.keys()
        assert request_dict["id"] == request_dict["id"]
        assert "user_id" in request_dict.keys()
        assert request_dict["user_id"] == request_dict["user_id"]
        assert "image_id" in request_dict.keys()
        assert request_dict["image_id"] == request_dict["image_id"]
        assert "reason" in request_dict.keys()
        assert request_dict["reason"] == request_dict["reason"]
        assert "status" in request_dict.keys()
        assert request_dict["status"] == request_dict["status"]

def test_requests_database_clear() -> None:
    """This function tests the functionality of the Database clear function"""
    db = Database()
    assert db.clear()
