from flask import request, jsonify # type: ignore
from classes.email import Email
import os
from dotenv import load_dotenv

load_dotenv()
sender_email_address = os.getenv("SENDER_EMAIL_ADDRESS")
app_password = os.getenv("SENDER_EMAIL_ADDRESS_APP_PASSWORD")

def send_email():
    """
    Description: Handling the POST /api/v2/emails endpoint.
    Input: JSON with 'receiver_email_address', 'subject' and 'body' key.
    Output: JSON with 'message' key describing status of the process.
    """

    data = request.json

    # Check for required keys
    required_keys = ['receiver_email_address', 'subject', 'body']
    for key in required_keys:
        if key not in data:
            return jsonify({"message": f"Missing required key: {key}"}), 400

    receiver_email_address = data['receiver_email_address']
    subject = data['subject']
    body = data['body']

    email_obj = Email(sender_email_address, app_password)
    if email_obj.send(receiver_email_address, subject, body):
        return jsonify({"message": "Email sent successfully!"}), 200
    else:
        return jsonify({"message": "Email failed to send!"}), 500
