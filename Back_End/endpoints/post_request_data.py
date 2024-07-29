from bottle import request, response # type: ignore

def post_request_data(db):
    data = request.json
    
    if not data or 'guest_id' not in data or 'img_id' not in data or 'reason' not in data:
        response.status = 400
        return {"error": "request_data parameter is required"}
    
    db.set_table_name('request')
    if not db.insert({
        "guest_id": int(data['guest_id']),
        "img_id": int(data['img_id']),
        "reason": str(data['reason']),
        "status": 0 # Pending
        }):
        response.status = 500
        return {"error": "db request insert cmd failed to execute"}
    
    response.status = 200
    return {'message': 'db insert request cmd executed successfully'}
