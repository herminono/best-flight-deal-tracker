import requests_cache
from pprint import pprint
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager

requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
pprint(sheet_data)

customer_data = data_manager.get_customer_emails()
customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]

how_many_days_before_go = int(input("How many days before go? "))
how_many_days_before_back = int(input("How many days after back? "))
if how_many_days_before_go > how_many_days_before_back:
    raise ValueError("Return date must be after departure date.")
go = datetime.now() + timedelta(days=how_many_days_before_go)
back = datetime.now() + timedelta(days=how_many_days_before_back)

notification_manager = NotificationManager()
flight_search = FlightSearch()
where_from = input("Enter origin airport: ").upper()
for destination in sheet_data:
    pprint(f'Getting direct flights for {destination["city"]}...')
    flights = flight_search.check_flight(
        where_from,
        destination["iataCode"],
        from_time = go,
        to_time = back,
    )

    cheapest_flight = find_cheapest_flight(flights,return_date=back.strftime("%Y-%m-%d"))
    pprint(f'{destination['city']}: IDR {cheapest_flight.price}')
    is_direct_flight = True
    if cheapest_flight.price == "N/A":
        is_direct_flight = False
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flight_search.check_flight(
            where_from,
            destination["iataCode"],
            from_time = go,
            to_time = back,
            is_direct = False,
        )

        cheapest_flight = find_cheapest_flight(stopover_flights, return_date=back.strftime("%Y-%m-%d"))
        pprint(f'Cheapest indirect flight to {sheet_data[0]['city']} is: IDR {cheapest_flight.price}')

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        if is_direct_flight:
            message = f"Low price alert! ({cheapest_flight.airline}) Only IDR {cheapest_flight.price} to fly direct "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! ({cheapest_flight.airline}) Only IDR {cheapest_flight.price} to fly " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"with {cheapest_flight.stops} stop(s) " \
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        notification_manager.send_email(customer_email_list, message)

        data_manager.update_lowest_price(
            row_id=destination["id"],
            new_price=cheapest_flight.price
        )

        print(f"Check your email. Lower price flight found to {destination['city']}.")

