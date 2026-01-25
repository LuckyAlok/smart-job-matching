import requests
import json

url = "http://127.0.0.1:8000/auth/register"
data = {
    "email": "debug_user_3@example.com",
    "password": "password"
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
