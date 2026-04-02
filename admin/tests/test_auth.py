import requests
import uuid

def test_trade_signup_and_login():
    base_url = "http://localhost:8002"
    signup_url = f"{base_url}/signup"
    login_url = f"{base_url}/login"
    unique = str(uuid.uuid4().int)[:8]  # Use only digits
    user = {
        "username": f"tradeuser_{unique}",
        "password": "TestPass123!",
        "email": f"trade{unique}@example.com",
        "phone_number": f"90000{unique[:4]}",
        "full_name": "Trade User Test",
        "aadhar_number": f"{100000000000+int(unique[:6]):012d}",
        "gst_number": f"GST{unique}TRADE",
        "gst_verified": False,
        "email_verified": False,
        "aadhar_verified": False
    }
    resp = requests.post(signup_url, json=user)
    print("Trade signup:", resp.status_code, resp.json())
    assert resp.status_code == 200
    login_data = {"email_or_phone": user["email"], "password": user["password"]}
    resp = requests.post(login_url, json=login_data)
    print("Trade login:", resp.status_code, resp.json())
    assert resp.status_code == 200
    assert "access_token" in resp.json()

def test_transport_signup_and_login():
    base_url = "http://localhost:8003"
    signup_url = f"{base_url}/signup"
    login_url = f"{base_url}/login"
    unique = str(uuid.uuid4().int)[:8]  # Use only digits
    user = {
        "username": f"transportuser_{unique}",
        "password": "TestPass123!",
        "email": f"transport{unique}@example.com",
        "phone_number": f"80000{unique[:4]}",
        "full_name": "Transport User Test",
        "aadhar_number": f"{200000000000+int(unique[:6]):012d}",
        "gst_number": f"GST{unique}TRANSPORT",
        "gst_verified": False,
        "email_verified": False,
        "aadhar_verified": False
    }
    resp = requests.post(signup_url, json=user)
    print("Transport signup:", resp.status_code, resp.json())
    assert resp.status_code == 200
    login_data = {"email_or_phone": user["email"], "password": user["password"]}
    resp = requests.post(login_url, json=login_data)
    print("Transport login:", resp.status_code, resp.json())
    assert resp.status_code == 200
    assert "access_token" in resp.json()

if __name__ == "__main__":
    test_trade_signup_and_login()
    test_transport_signup_and_login()
