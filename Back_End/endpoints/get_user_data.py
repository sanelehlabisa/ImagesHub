from bottle import response # type: ignore
import json
from classes import User_Data

def get_user_data(db, user_id):
    db.set_table_name('guest')
    guest_user = db.read({'id': user_id})

    if guest_user:
        response.status = 200
        user = User_Data(guest_user[0][0], guest_user[0][1], 1).__dict__

        return json.dumps(user)

    # User not found
    response.status = 404
    return {'error': 'User not found'}
