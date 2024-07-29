import requests # type: ignore
import os

GREEN_TICK = '\033[92m✔\033[0m'  # green color tick
RED_CROSS = '\033[91m✖\033[0m'  # red color cross

def test_serve_image(n, filename="low_res_DEEP2heat_cropped.jpg"):
    url = f"http://localhost:8080/api/serve-image/{filename}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    # Test GET request
    response = requests.get(url, headers=headers)
    try:
        assert response.status_code == 200
        assert response.headers['Content-Type'].startswith('image/')
        print(f"{GREEN_TICK} Test {n} passed!")
    except AssertionError:
        print(f"{RED_CROSS} Test {n} failed!")
        print(response.text)