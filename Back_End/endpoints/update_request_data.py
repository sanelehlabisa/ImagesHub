from bottle import request, response # type: ignore

def update_request_data(db):
    data = request.json
    if not data or 'id' not in data or 'guest_id' not in data or 'status' not in data:
        response.status = 400
        return {"error": "id and request_data parameters are required"}
    
    db.set_table_name('request')
    if not db.update({
            'status':str(data['status'])
        },{
            'id': str(data['id'])
        }):
        response.status = 500
        return {"error": "db request update cmd failed to execute"}
    
    response.status = 200
    return {'message': 'db update request cmd executed successfully'}
