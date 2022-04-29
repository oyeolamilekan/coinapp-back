import requests
from django.utils.crypto import get_random_string
from decouple import config


class BillApiProvider:
    def __init__(self, api_keys) -> None:
        self.api_keys = api_keys
        self.base_url = "https://api.flutterwave.com/v3/bills"
        self.headers = {
            "Authorization": f"Bearer {self.api_keys}",
            "Content-Type": "application/json",
        }

    def buy_airtime(self, phone_number, amount):
        data = {
            "country": "NG",
            "customer": phone_number,
            "amount": amount,
            "type": "AIRTIME",
            "reference": get_random_string(length=20),
        }
        request = requests.post(
            self.base_url,
            json=data,
            headers=self.headers,
        )
        return request.json()

bill = BillApiProvider(config("BILL_PROVIDER"))