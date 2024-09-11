from flask import request, jsonify
from classes.send_email import Email
import os

def send_email():
    sender_email_address = os.getenv("SENDER_EMAIL_ADDRESS")
    app_password = os.getenv("SENDER_EMAIL_ADDRESS_APP_PASSWORD")

    # Get JSON data from request
    data = request.json

    # Check for required keys
    required_keys = ['receiver_email_address', 'subject', 'body']
    for key in required_keys:
        if key not in data:
            response.status_code = 400
            return jsonify({"error": f"Missing required key: {key}"}), 400

    receiver_email_address = data['receiver_email_address']
    subject = data['subject']
    body = data['body']

    email_obj = Email(sender_email_address, app_password)
    if email_obj.send(receiver_email_address, subject, body):
        return jsonify({"message": "Email sent successfully!"}), 200
    else:
        return jsonify({"error": "Email failed to send!"}), 500
