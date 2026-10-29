# best-flight-deal-tracker
This is a python-based flight price tracking application that searches for the cheapest flights and sends email notifications when prices fall below predefined thresholds.
Features:
1. Searches flight prices using SerpAPI.
2. Compares flight prices against thresholds stored in Google Sheets through Sheety and updates it when a cheaper price is found.
3. Searches for connecting flights when no direct flights are found.
4. Sends email notifications for cheap flight deals.
5. Use SQLite-based request caching to reduce repeated API calls and save tokens.
Technologies Used:
1. Python
2. SerpAPI
3. Sheety API
4. Requests and Requests-Cache
5. SMTP
6. SQLite
How it works:
1. Retrieves destination data and price thresholds from Google Sheets.
2. Accepts an origin airport and the interval of travel dates.
3. Searches for available flight options.
4. Identifies the cheapest flight.
5. Compares the price against the stored threshold.
6. Sends an email alert when a cheapest flight is detected.
Project Status:
Personal learning project. Additional improvements include error handling and additional features.
