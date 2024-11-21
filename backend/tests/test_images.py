"""This file is responsible for testing the images enpoint using pytest"""
import os
import json
from dotenv import load_dotenv
from main import app
from classes import Database

URL = "http://localhost:5000/api/v2/images"
load_dotenv()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}"
}

def test_post_image() -> None:
    """This function tests the functionality of POST images endpoint"""
    image_data = {
        "img_path": "./res/Heat-wave.jpg"
    }

    with app.test_client() as client:
        response = client.post(URL, headers=headers, json=image_data)
        image_dict = response.get_json()
        image_fname = image_data['img_path'].rsplit('/', maxsplit=1)[-1]

        assert response.status_code == 200
        assert isinstance(image_dict, dict)
        assert "low_res_img_fname" in image_dict.keys()
        assert image_fname in image_dict["low_res_img_fname"]
        assert "high_res_img_fname" in image_dict.keys()
        assert image_fname in image_dict["high_res_img_fname"]   

def test_get_images() -> None:
    """This function tests the functionality of the GET images endpoint."""
    image_data = {}

    with app.test_client() as client:
        response = client.get(URL, headers=headers, json=image_data)
        images_list = response.get_json()

        assert response.status_code == 200
        assert isinstance(images_list, list)
        for image_dict in images_list:
            assert "id" in image_dict.keys()
            assert "low_res_img_fname" in image_dict.keys()
            assert "high_res_img_fname" in image_dict.keys()
            assert "metadata" in image_dict.keys()

def test_put_image() -> None:
    """This function tests the functionality of the PUT image endpoint"""
    image_data = {
        "id": 1,
        "low_res_img_fname": "test_low_img_fname_updated",
        "high_res_img_fname": "test_high_img_fname_updated",
        "metadata": "{}"
    }

    with app.test_client() as client:
        response = client.put(URL, headers=headers, data=json.dumps(image_data))
        image_dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(image_dict, dict)
        assert "message" in image_dict.keys()
        assert "Image updated successfully!" in image_dict["message"]
        assert "id" in image_dict.keys()
        assert image_data["id"] == image_dict["id"]
        assert "low_res_img_fname" in image_dict.keys()
        assert image_data["low_res_img_fname"] == image_dict["low_res_img_fname"]
        assert "high_res_img_fname" in image_dict.keys()
        assert image_data["high_res_img_fname"] == image_dict["high_res_img_fname"]
        assert "metadata" in image_dict.keys()
        assert image_data["metadata"] == image_dict["metadata"]

def test_delete_image() -> None:
    """This function tests the functionality of the DELETE image endpoint"""
    image_data = {
        "id": 1,
        "low_res_img_fname": "test_low_img_fname",
        "high_res_img_fname": "test_high_img_fname",
        "metadata": "{}"
    }

    with app.test_client() as client:
        response = client.delete(URL, headers=headers, json=image_data)
        image_dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(image_dict, dict)
        assert "message" in image_dict.keys()
        assert "Image deleted successfully!" in image_dict["message"]
        assert "id" in image_dict.keys()
        assert image_data["id"] == image_dict["id"]
        assert "low_res_img_fname" in image_dict.keys()
        assert image_data["low_res_img_fname"] == image_dict["low_res_img_fname"]
        assert "high_res_img_fname" in image_dict.keys()
        assert image_data["high_res_img_fname"] == image_dict["high_res_img_fname"]
        assert "metadata" in image_dict.keys()
        assert image_data["metadata"] == image_dict["metadata"]

def test_images_database_clear() -> None:
    """This function tests the functionality of the Database clear function"""
    db = Database()
    assert db.clear()
