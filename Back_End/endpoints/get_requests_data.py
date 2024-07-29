from bottle import response # type: ignore
import json
from classes.request_data import Request_Data

def get_requests_data(db):
    db.set_table_name('request')
    requests = db.read()

    if not requests:
        response.status = 404
        return {'error': 'no requests found'}

    response.status = 200
    req_data_list = list()
    for req in requests:
        req_data_list.append(Request_Data(int(req[0]), int(req[1]), int(req[2]), str(req[3]), int(req[4])).__dict__)
    return json.dumps(req_data_list)
