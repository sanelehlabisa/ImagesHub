from bottle import response  # type: ignore
from classes.user_data import User_Data
import json

def get_users_data(db):
    db.set_table_name('administrator')
    admin_users = db.read()
    db.set_table_name('guest')
    guest_users = db.read()

    response.status = 200
    users = []

    for user in admin_users:
        users.append(User_Data(user[0], user[1], 1).__dict__)

    for user in guest_users:
        users.append(User_Data(user[0], user[1], 0).__dict__)

    return json.dumps(users)