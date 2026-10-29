class FlightData:
    def __init__(self,price,origin_airport,destination_airport,out_date,return_date, stops=0, airline="Unknown"):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops
        self.airline = airline

def find_cheapest_flight(data,return_date):
    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("No flight data found")
        return FlightData("N/A","N/A","N/A","N/A","N/A")

    all_flights = (
            (data.get("best_flights") or [])
            + (data.get("other_flights") or [])
    )
    print(f"Found {len(all_flights)} flights options")

    valid_flights = [
        flight for flight in all_flights
        if isinstance(flight.get("price"), (int, float))
           and flight.get("flights")
    ]

    if not valid_flights:
        print("No valid flight data found")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = min(
        valid_flights,
        key=lambda flight: flight["price"]
    )
    airline = first_flight["flights"][0].get("airline", "Unknown")

    lowest_price = first_flight["price"]
    origin = first_flight["flights"][0]["departure_airport"]["id"]
    destination = first_flight["flights"][-1]["arrival_airport"]["id"]
    out_date = first_flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
    nr_stops = len(first_flight["flights"]) - 1

    cheapest_flight = FlightData(
        lowest_price,
        origin,
        destination,
        out_date,
        return_date,
        stops=nr_stops,
        airline=airline
    )

    for flight in all_flights:
        try:
            price = flight["price"]
        except KeyError:
            print("No price available for flight.")
            continue
        if price < lowest_price:
            lowest_price = price
            origin = flight["flights"][0]["departure_airport"]["id"]
            destination = flight["flights"][-1]["arrival_airport"]["id"]
            out_date = flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
            nr_stops = len(first_flight["flights"])-1
            cheapest_flight = FlightData(lowest_price,origin,destination,out_date,return_date,stops=nr_stops)
            print(f'Lowest price to {destination} is IDR {lowest_price}')

    return cheapest_flight


