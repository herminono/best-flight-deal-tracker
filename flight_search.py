import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_ENDPOINT = os.environ["SERPAPI_ENDPOINT"]

class FlightSearch:
    def __init__(self):
        self.is_direct = True
        self._api_key = os.environ["SERPAPI_KEY"]

    def check_flight(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        query = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"),
            "return_date": to_time.strftime("%Y-%m-%d"),
            "type": "1",
            "adults": "1",
            "currency": "IDR",
            "api_key": self._api_key,
        }
        if is_direct:
            query["stops"]="1"
        response = requests.get(url=SERPAPI_ENDPOINT, params=query, timeout=30)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None

        data = response.json()
        if "error" in data:
            print(f'API Error: {data["error"]}')
            return None
        return data