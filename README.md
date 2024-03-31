# Crypto Price Tracker

1. Import the migration file to create the tables
2. Make sure to have currency API's (https://currencyapi.com) API key (used to retrieve the latest IDR currency rate from USD)
3. Run the API with `python3 -m uvicorn src.main:app --reload --port 50000`
