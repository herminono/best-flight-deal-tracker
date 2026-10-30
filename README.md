# Flight Deal Tracker ✈️

A Python command-line application that searches for round-trip flights, compares fares against target prices stored in Google Sheets, and sends email alerts when it finds a cheaper option.

This project integrates external APIs, spreadsheet-based data management, and SMTP email notifications.

## Features

- Searches Google Flights results through **SerpApi**.
- Reads destination airport codes and target prices from **Google Sheets** through **Sheety**.
- Accepts an origin airport code and departure/return dates as offsets from today.
- Finds the cheapest available itinerary in the returned flight results.
- Compares the fare with each destination's stored price threshold.
- Sends email alerts to addresses retrieved from a separate Sheety users sheet.
- Uses `requests-cache` to cache flight API responses for one hour, while excluding Sheety requests from the cache.

> **Project status:** This is a learning project. The current code includes an indirect-flight fallback path, but that path needs fixes before it can be considered reliable (see Known Limitations).

## Tech Stack

- Python
- [SerpApi](https://serpapi.com/) (Google Flights search results)
- [Sheety](https://sheety.co/) (Google Sheets REST API)
- `requests`, `requests-cache`
- `python-dotenv`
- `smtplib` (SMTP email notifications)

## Project Structure

```text
flight-deal-tracker/
├── main.py                  # CLI input, search orchestration, and alert conditions
├── data_manager.py          # Sheety API integration
├── flight_search.py         # SerpApi flight requests
├── flight_data.py           # Flight model and cheapest-flight selection
├── notification_manager.py  # SMTP email alerts
├── requirements.txt         # Python dependencies (create if not present)
├── .gitignore
└── README.md
```

A `flight_cache.sqlite` database may be generated during execution and does not need to be committed.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the placeholder with your actual repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install requests requests-cache python-dotenv
```

Optionally record the project dependencies in `requirements.txt` and install them using `pip install -r requirements.txt`.

### 4. Configure external services

1. Create a SerpApi account and obtain an API key for Google Flights requests.
2. Set up Sheety access to a Google Sheet with a `prices` resource, containing at least `city`, `iataCode`, and `lowestPrice` columns.
3. Set up a Sheety `users` resource containing the email addresses to notify. The current code expects the JSON field `whatIsYourEmail?`.
4. Configure an SMTP email account. Depending on your provider, an app password or other provider-specific configuration may be required.

Example `prices` sheet:

| city | iataCode | lowestPrice |
|---|---|---:|
| Singapore | SIN | 1500000 |
| Tokyo | NRT | 4500000 |

These are illustrative values, not real-time flight prices.

### 5. Create a `.env` file

Create `.env` in the project's root directory:

```dotenv
SERPAPI_ENDPOINT=https://serpapi.com/search
SERPAPI_KEY=your_serpapi_key

SHEETY_ENDPOINT=your_sheety_prices_endpoint
SHEETY_PUT_ENDPOINT=your_sheety_prices_endpoint
SHEETY_USERS_ENDPOINT=your_sheety_users_endpoint
SHEETY_USERNAME=your_sheety_username
SHEETY_PASSWORD=your_sheety_password

EMAIL_PROVIDER_SMTP_ADDRESS=your_smtp_host
MY_EMAIL=your_email_address
MY_EMAIL_PASSWORD=your_email_app_password
```

**Never commit actual credentials.** The current notification code opens the SMTP connection without specifying a port and then calls `starttls()`. Your SMTP provider must support this connection pattern, or the code must be adjusted for its port and TLS requirements.

### 6. Run the program

```bash
python main.py
```

The command-line program asks for:

- Number of days from today until departure
- Number of days from today until return
- Origin airport code (for example, `YIA`)

It then searches the destinations listed in the Sheet and sends an email if a returned fare is lower than the destination's stored threshold.

## How It Works

1. `DataManager` reads destination records and recipient emails from Sheety.
2. The user enters an origin airport and relative departure/return dates.
3. `FlightSearch` requests round-trip Google Flights results from SerpApi using IDR as the currency.
4. `find_cheapest_flight()` examines the returned `best_flights` and `other_flights` lists and selects the lowest-priced result.
5. `main.py` compares that price with the corresponding destination's `lowestPrice`.
6. `NotificationManager` emails the registered recipients when the fare is below the threshold.

## Example Alert

```text
Subject: New Low Price Flight!

Low price alert! (Lion) Only IDR 1200000 to fly direct from CGK to SIN,
on 2026-11-15 until 2026-11-20.
```

Illustrative only; this is not a live quote.

## License

The code is available for portfolio review; no additional reuse permissions are granted by this README.
