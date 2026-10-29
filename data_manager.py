import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

SHEETY_ENDPOINT =os.environ["SHEETY_ENDPOINT"]
SHEETY_PUT_ENDPOINT = os.environ["SHEETY_PUT_ENDPOINT"]
SHEETY_USERS_ENDPOINT = os.environ["SHEETY_USERS_ENDPOINT"]

class DataManager:
    def __init__(self):
        self._user = os.environ['SHEETY_USERNAME']
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.users_endpoint = SHEETY_USERS_ENDPOINT
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_ENDPOINT, auth=self._authorization)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_lowest_price(self,row_id,new_price):
        new_data = {
            "price": {
                "lowestPrice": new_price
            },
        }
        response = requests.put(
            url=f'{SHEETY_PUT_ENDPOINT}/{row_id}',
            json=new_data,
            auth=self._authorization,
            timeout=30
        )
        response.raise_for_status()
        print(f"Successfully updated row {row_id}!")

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, auth=self._authorization)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data

