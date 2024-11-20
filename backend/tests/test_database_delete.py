"""This file is responsible for testing the delete function from database class"""
from classes import Database


def test_database_insert() -> None:
    """This function tests the functionality of the delete to database function"""
    db = Database()
    
    assert "testing" in db.name
    assert db.clear() == True