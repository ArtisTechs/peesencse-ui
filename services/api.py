import requests

BASE_URL = "http://127.0.0.1:5000"

def analyze_sample(name, age, sex, image_path):
    with open(image_path, "rb") as f:
        files = {"image": f}
        data = {
            "name": name,
            "age": age,
            "sex": sex
        }

        response = requests.post(
            f"{BASE_URL}/analyze",
            data=data,
            files=files
        )

    return response.text

def get_users():
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print("API Error:", e)

    return []