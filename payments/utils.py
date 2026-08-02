import requests, base64, os
from datetime import datetime
from requests.auth import HTTPBasicAuth

CONSUMER_KEY = os.environ.get("MPESA_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("MPESA_CONSUMER_SECRET")
SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
BASE_URL = "https://sandbox.safaricom.co.ke"

def get_access_token():
    auth_url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json()["access_token"]

def build_password():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = SHORTCODE + PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode()
    return password, timestamp

def initiate_stk_push(phone_number, amount, callback_url, account_reference):
    access_token = get_access_token()
    password, timestamp = build_password()

    stk_url = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": "AzureYacht Booking Payment"
    }

    response = requests.post(stk_url, json=payload, headers=headers)
    return response.json()