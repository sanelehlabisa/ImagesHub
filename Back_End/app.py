from bottle import Bottle, response, request # type: ignore
import os
from classes.db_table import DB_Table
from classes.gmail import Gmail
from endpoints import get_users_data, sign_in, post_image_data, get_images_data, get_image_data, serve_image, post_request_data, get_request_data, get_requests_data, update_request_data, get_user_data
from dotenv import load_dotenv

class ImageHubApp:
    def __init__(self, db_name):
        self.app = Bottle()
        self.db = DB_Table(db_name)
        self.api_key = os.getenv('API_KEY')
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/api/get-user-data/<id:int>', method=["GET", "OPTIONS"], callback=self.enable_cors(self.get_user_data))
        self.app.route("/api/get-users-data", method=["GET", "OPTIONS"], callback=self.enable_cors(self.get_users_data))
        self.app.route("/api/sign-in", method=["POST", "OPTIONS"], callback=self.enable_cors(self.sign_in))
        self.app.route('/api/post-image-data', method=["POST", "OPTIONS"], callback=self.enable_cors(self.post_image_data))
        self.app.route('/api/serve-image/<filename:path>', method=["GET", "OPTIONS"], callback=self.enable_cors(self.serve_image))
        self.app.route('/api/get-image-data/<id:int>', method=["GET", "OPTIONS"], callback=self.enable_cors(self.get_image_data))
        self.app.route('/api/get-images-data', method=["GET", "OPTIONS"], callback=self.enable_cors(self.get_images_data))
        self.app.route('/api/post-request-data', method=["POST", "OPTIONS"], callback=self.enable_cors(self.post_request_data))
        self.app.route('/api/get-request-data/<id:int>', method=["GET", "OPTIONS"], callback=self.enable_cors(self.get_request_data))
        self.app.route('/api/get-requests-data', method=["GET", "OPTIONS"], callback=self.enable_cors(self.get_requests_data))
        self.app.route('/api/update-request-data', method=["PUT", "OPTIONS"], callback=self.enable_cors(self.update_request_data))
        self.app.hook('after_request')(self.add_cors_headers)

    def validate_api_key(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            response.status = 403
            return {'error': 'Forbidden'}
        api_key = auth_header.split(" ")[1]
        if api_key != self.api_key:
            response.status = 403
            return {'error': 'Forbidden'}

    def enable_cors(self, fn):
        def _enable_cors(*args, **kwargs):
            if request.method == 'OPTIONS':
                self.add_cors_headers()
                response.status = 200
                return {}
            self.validate_api_key()
            self.add_cors_headers()
            return fn(*args, **kwargs)
        return _enable_cors

    def add_cors_headers(self):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, Authorization, X-Requested-With, X-CSRF-Token, API_KEY'

    def get_user_data(self, id):
        return get_user_data(self.db, id)

    def get_users_data(self):
        return get_users_data(self.db)

    def sign_in(self):
        return sign_in(self.db)

    def post_image_data(self):
        return post_image_data(self.db)

    def serve_image(self, filename):
        return serve_image(filename)

    def get_image_data(self, id):
        return get_image_data(self.db, id)

    def get_images_data(self):
        return get_images_data(self.db)

    def post_request_data(self):
        load_dotenv()
        sender_email_address = os.getenv("SENDER_EMAIL_ADDRESS") # "your_sender_email@example.com"
        receiver_email_address = os.getenv("RECEIVER_EMAIL_ADDRESS") # "your_receiver_email@example.com"
        
        if not sender_email_address or not receiver_email_address:
            print("Error: Missing email addresses. Check environment variables.")
            return

        gmail = Gmail(sender_email_address)
        gmail.send(receiver_email_address)
        return post_request_data(self.db)

    def get_request_data(self, id):
        return get_request_data(self.db, id)

    def get_requests_data(self):
        return get_requests_data(self.db)

    def update_request_data(self):
        return update_request_data(self.db)

if __name__ == "__main__":
    app = ImageHubApp("images_hub.db")
    app.app.run(host="0.0.0.0", port=8080, debug=True)

