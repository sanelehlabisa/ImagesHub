from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv
import os
from epoints.emails import send_email

app = Flask(__name__)
load_dotenv()

class Back_End:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')

    def validate_api_key(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return self.forbidden_response()
        api_key = auth_header.split(" ")[1]
        
        if api_key != self.api_key:
            return self.forbidden_response()

    def forbidden_response(self):
        return jsonify({'error': 'Forbidden'}), 403

    def enable_cors(self, fn):
        def _enable_cors(*args, **kwargs):
            if request.method == 'OPTIONS':
                self.add_cors_headers()
                return {}, 200  # No content for preflight requests
            validation_response = self.validate_api_key()
            if validation_response:
                return validation_response
            self.add_cors_headers()
            return fn(*args, **kwargs)
        return _enable_cors

    def add_cors_headers(self):
        response = Response()  # Create a new Response object
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, Authorization, X-Requested-With, X-CSRF-Token, API_KEY'
        return response

backend = Back_End()

@app.route('/api/v2/emails', methods=['POST'])
@backend.enable_cors
def send_email_route():
    return send_email()

if __name__ == '__main__':
    app.run(debug=True)
