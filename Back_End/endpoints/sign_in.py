from bottle import request, response # type: ignore
from classes.user_data import User_Data
import json

def sign_in(db):
    data = request.json
    if not data or 'email_address' not in data:
        response.status = 400
        return {"error": "email_address parameter is required"}
    
    email_address = data['email_address']
    id, email, t = (0, '', '')

    db.set_table_name('administrator')
    admin_result = db.read({'email_address': email_address})
    if admin_result:
        (id, email), t = admin_result[0], 0
    else:    
        db.set_table_name('guest')
        guest_result = db.read({'email_address': email_address})
        if guest_result:
            (id, email), t = guest_result[0], 1
        else:
            db.set_table_name('guest')
            if db.insert({'email_address': email_address}):
                new_guest = db.read({'email_address': email_address})
                if new_guest:
                    (id, email), t = new_guest[0], 1
                
    if id:
        response.status = 200
        user = User_Data(id, email, t)
        return json.dumps(user.toJSON())
    else:
        response.status = 500
        return {"error": "db insert user cmd failed to execute"}
