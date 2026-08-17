import requests

response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={"message": "Where is my order ORD-123?"}
)

print(response.json())