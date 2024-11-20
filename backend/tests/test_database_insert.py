"""This file is responsible for testing the insert function from database class"""
from classes import Database


def test_database_insert() -> None:
    """This function tests the functionality of the insert to database function"""
    db = Database()
    user = {
        "id": 1,
        "email_address": "test@sarao.ac.za",
        "type": 2
    }
    
    assert "testing" in db.name
    assert db.insert("user", user) == True
    