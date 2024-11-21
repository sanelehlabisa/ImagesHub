"""This file is responsible for testing the links enpoint using pytest"""
import os
import json
from dotenv import load_dotenv
from main import app
from classes import Database

URL = "http://localhost:5000/api/v2/links"
load_dotenv()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}"
}

def test_post_link() -> None:
    """This function tests the functionality of POST links endpoint"""
    link_data = {
        'image_id': 1,
        'key': 'test_key',
        'limit': 5
    }    

    with app.test_client() as client:
        response = client.post(URL, headers=headers, json=link_data)
        link_dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(link_dict, dict)
        assert "image_id" in link_dict.keys()
        assert link_dict["image_id"] == link_dict["image_id"]
        assert "key" in link_dict.keys()
        assert link_dict["key"] == link_dict["key"]
        assert "limit" in link_dict.keys()
        assert link_dict["limit"] == link_dict["limit"]

def test_get_links() -> None:
    """This function tests the functionality of the GET links endpoint."""
    link_data = {}

    with app.test_client() as client:
        response = client.get(URL, headers=headers, json=link_data)
        link_list: list[dict] = response.get_json()

        assert response.status_code == 200
        assert isinstance(link_list, list)
        for link_dict in link_list:
            assert "id" in link_dict.keys()
            assert "image_id" in link_dict.keys()
            assert "key" in link_dict.keys()
            assert "limit" in link_dict.keys()

def test_put_link() -> None:
    """This function tests the functionality of the PUT link endpoint"""
    link_data = {
        'id': 1,
        'image_id': 1,
        'key': 'test_key',
        'limit': 5
    }

    with app.test_client() as client:
        response = client.put(URL, headers=headers, data=json.dumps(link_data))
        link_dict: dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(link_dict, dict)
        assert "message" in link_dict.keys()
        assert "Link updated successfully!" in link_dict["message"]
        assert "id" in link_dict.keys()
        assert link_dict["id"] == link_dict["id"]
        assert "image_id" in link_dict.keys()
        assert link_dict["image_id"] == link_dict["image_id"]
        assert "key" in link_dict.keys()
        assert link_dict["key"] == link_dict["key"]
        assert "limit" in link_dict.keys()
        assert link_dict["limit"] == link_dict["limit"]

def test_delete_link() -> None:
    """This function tests the functionality of the DELETE links endpoint"""
    link_data = {
        'id': 1,
        'image_id': 1,
        'key': 'test_key',
        'limit': 5
    }

    with app.test_client() as client:
        response = client.delete(URL, headers=headers, json=link_data)
        link_dict: dict = response.get_json()
        
        assert response.status_code == 200
        assert isinstance(link_dict, dict)
        assert "message" in link_dict.keys()
        assert "Link deleted successfully!" in link_dict["message"]
        assert "id" in link_dict.keys()
        assert link_dict["id"] == link_dict["id"]
        assert "image_id" in link_dict.keys()
        assert link_dict["image_id"] == link_dict["image_id"]
        assert "key" in link_dict.keys()
        assert link_dict["key"] == link_dict["key"]
        assert "limit" in link_dict.keys()
        assert link_dict["limit"] == link_dict["limit"]

def test_requests_database_clear() -> None:
    """This function tests the functionality of the Database clear function"""
    db = Database()
    assert db.clear()
