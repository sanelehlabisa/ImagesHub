"""This file is responsible for testing the read function from database class"""
from classes import Database


def test_database_read() -> None:
    """This function tests the functionality of the read to database function"""
    db = Database()
    users = db.read("users")
    
    assert "testing" in db.name
    assert isinstance(users, list)