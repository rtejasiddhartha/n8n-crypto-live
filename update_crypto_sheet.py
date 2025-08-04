# update_crypto_sheet.py

import os
import json
import gspread
import requests
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Load credentials from the environment variable
service_account_info = json.loads(os.environ["GCP_CREDENTIALS"])

# Setup Google Sheets client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# Google Sheet ID and worksheet name (you must set these)
SHEET_ID = "YOUR_SHEET_ID"
WORKSHEET_NAME = "Sheet1"

# Fetch CoinGecko top 5 INR coins as an example
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 5,
    "page": 1,
    "price_change_percentage": "24h"
}
response = requests.get(url, params=params)
data = response.json()

# Open sheet
sheet = gc.open_by_key("1Yc1DidfDwlaLDT3rpAnEJII4Y1vbrfTe5Ub4ZEUylsg")
worksheet = sheet.worksheet("Crypto-workflow")

# Append rows
for coin in data:
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        coin["name"],
        coin["symbol"].upper(),
        f'₹{coin["current_price"]}',
        f'{coin["price_change_percentage_24h"]:.2f}%',
        f'₹{coin["market_cap"]}',
        f'₹{coin["total_volume"]}'
    ]
    worksheet.append_row(row, value_input_option="USER_ENTERED")