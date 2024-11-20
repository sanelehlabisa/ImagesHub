import os
import pytest
from dotenv import load_dotenv
from main import app

@pytest.fixture
def api_key() -> str:
    load_dotenv()
    return os.getenv("API_KEY")

def test_send_email(api_key) -> None:
    url = "http://localhost:5000/api/v2/emails"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "receiver_email_address": "shlabisa@sarao.ac.za",
        "subject": "Send Email Test",
        "body": "This is a test email from the Images Hub Team"
    }

    with app.test_client() as client:
        response = client.post(url, headers=headers, json=payload)
        response_dict = response.get_json()

        assert response.status_code == 200
        assert isinstance(response_dict, dict)
        assert "message" in response_dict
        assert response_dict["message"] == "Email sent successfully!"
