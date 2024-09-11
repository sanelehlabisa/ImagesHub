import requests  # type: ignore
import json
from dotenv import load_dotenv, set_key
import os

def test_send_email(params={}) -> bool:
    url = "http://localhost:5000/api/v2/emails" 

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
        return True
    except AssertionError:
        print(response_data)
        return False


if __name__ == "__main__":
    GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
    RED_CROSS = '\033[91m✖\033[0m'  # red color cross

    set_key('.env', 'DATABASE_NAME', "t_images_hub.db")

    if test_send_email():
        print(f"Send Email Test {GREEN_TICK} passed!")
    else:
        print(f"Send Email Test {RED_CROSS} failed!")

    set_key('.env', 'DATABASE_NAME', "images_hub.db")