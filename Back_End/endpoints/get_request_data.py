from bottle import response # type: ignore
import json
from classes import Request_Data

def get_request_data(db, id):
    db.set_table_name('request')
    request_data = db.read({'id': id})

    if not request_data:
        response.status = 404
        return {'error': 'request not found'}

    response.status = 200
    req_data = Request_Data(request_data[0][0], request_data[0][1], request_data[0][2], request_data[0][2], request_data[0][3]).__dict__

    return json.dumps(req_data)
