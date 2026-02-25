import requests

BASE_URL = "http://192.168.0.229:5000"

def analyze_sample(user_id, age, gender, image_path):
    with open(image_path, "rb") as f:
        files = {
            "image": ("sample.jpg", f, "image/jpeg")
        }

        data = {
            "user_id": user_id,
            "age": age,
            "gender": gender
        }

        response = requests.post(
            f"{BASE_URL}/analyze",
            data=data,
            files=files
        )

    if response.status_code != 201:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    payload = response.json()

    if not payload.get("success"):
        raise Exception(payload.get("error", "Unknown API error"))

    return {
        "user_id": payload.get("user_id"),
        "result_id": payload.get("result_id"),
        "result_url": payload.get("result_url"),
        "rbc": payload.get("rbc"),
        "wbc": payload.get("wbc"),
        "uti": payload.get("uti")
    }

def get_users():
    response = requests.get(f"{BASE_URL}/users")

    if response.status_code == 200:
        return response.json()

    raise Exception(f"API error: {response.status_code} {response.text}")
    

def create_user(firstname, middlename, lastname, age, gender):
    payload = {
        "firstname": firstname,
        "middlename": middlename,
        "lastname": lastname,
        "age": age,
        "gender": gender
    }

    response = requests.post(f"{BASE_URL}/info", json=payload)

    if response.status_code == 201:
        return response.json()

    raise Exception(response.text)


def fetch_users():
    response = requests.get(f"{BASE_URL}/users")

    if response.status_code == 200:
        return response.json()

    raise Exception(response.text)