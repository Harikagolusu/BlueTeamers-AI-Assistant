import requests

# Assuming demo token might not be needed if I just hit the API with some mock token to see if it 500s
try:
    res2 = requests.get("http://127.0.0.1:8001/api/chat/session", headers={"Authorization": f"Bearer mock_token"})
    print(f"Session API Status: {res2.status_code}")
    print(f"Session API Response: {res2.text}")
except Exception as e:
    print(f"Error: {e}")
