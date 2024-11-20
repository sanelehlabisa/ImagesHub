"""This file is responsible for testing the update function from database class"""
from classes import Database


def test_database_update() -> None:
    """This function tests the functionality of the update to database function"""
    db = Database()
    user = {
        "id": 1,
        "email_address": "test@sarao.ac.za",
        "type": 3
    }
    
    assert "testing" in db.name
    assert db.update("user", user, {"id": user["id"]}) == True
    