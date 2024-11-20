"""This file is responsible for testing the users enpoint using pytest"""
import os
import json
from dotenv import load_dotenv
from main import app
from classes import Database

URL = "http://localhost:5000/api/v2/users"
load_dotenv()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}"
}

def test_post_user() -> None:
    """This function tests the functionality of POST users endpoint"""
    user_data = {
        "email_address": "test@imageshub.ac.za",
        "type": 2
    }

    with app.test_client() as client:
        response = client.post(URL, headers=headers, json=user_data)
        user_dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(user_dict, dict)
        assert "message" in user_dict.keys()
        assert "User inserted successfully!" in user_dict["message"]
        assert "email_address" in user_dict.keys()
        assert user_data["email_address"] == user_dict["email_address"]
        assert "type" in user_dict.keys()
        assert user_data["type"] == user_dict["type"]

def test_get_users() -> None:
    """This function tests the functionality of the GET users endpoint."""
    user_data = {}

    with app.test_client() as client:
        response = client.get(URL, headers=headers, json=user_data)
        users_list = response.get_json()

        assert response.status_code == 200
        assert isinstance(users_list, list)
        for user_dict in users_list:
            assert "id" in user_dict.keys()
            assert "email_address" in user_dict.keys()
            assert "type" in user_dict.keys()

def test_put_user() -> None:
    """This function tests the functionality of the PUT users endpoint"""
    user_data = {
        "id": 1,
        "email_address": "test@imageshub.ac.za",
        "type": 2
    }

    with app.test_client() as client:
        response = client.put(URL, headers=headers, data=json.dumps(user_data))
        user_dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(user_dict, dict)
        assert "message" in user_dict.keys()
        assert "User updated successfully!" in user_dict["message"]
        assert "email_address" in user_dict.keys()
        assert user_data["email_address"] == user_dict["email_address"]
        assert "type" in user_dict.keys()
        assert user_data["type"] == user_dict["type"]

def test_delete_user() -> None:
    """This function tests the functionality of the DELETE users endpoint"""
    user_data = {
        "id": 1,
        "email_address": "test@imageshub.ac.za",
        "type": 2
    }

    with app.test_client() as client:
        response = client.delete(URL, headers=headers, json=user_data)
        user_dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(user_dict, dict)
        assert "message" in user_dict.keys()
        assert "User deleted successfully!" in user_dict["message"]
        assert "email_address" in user_dict.keys()
        assert user_data["email_address"] == user_dict["email_address"]
        assert "type" in user_dict.keys()
        assert user_data["type"] == user_dict["type"]

def test_database_clear() -> None:
    """This function tests the functionality of the DB clear function"""
    db = Database()
    assert db.clear() == True