import requests  # type: ignore
import json
from dotenv import load_dotenv
import os


GREEN_TICK = '\033[92m✔\033[0m'
RED_CROSS = '\033[91m✖\033[0m'

def test_send_email(n):
    url = "http://localhost:5000/api/v2/emails"  # Update the port if necessary

    load_dotenv()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    # Sample payload for sending email
    payload = {
        "receiver_email_address": "shlabisa@sarao.ac.za",
        "subject": "Send Email Test",
        "body": "This is a test email from the Images Hub Team"
    }

    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()

    try:
        assert response.status_code == 200
        assert isinstance(response_data, dict)
        assert 'message' in response_data
        assert response_data['message'] == "Email sent successfully!"
        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError:
        print(f"{RED_CROSS} Test {n} failed!")
        print(response_data)

# Example usage
if __name__ == "__main__":
    test_send_email(1)
