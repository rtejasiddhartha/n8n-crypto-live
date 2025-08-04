# fetch_and_update.py

import requests
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# ---- Google Sheets Setup ----
SHEET_NAME = "CryptoPulseAlerts"
WORKSHEET_NAME = "Sheet1"
CREDENTIALS_FILE = "credentials.json"  # Put this in the root of your repo

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
gc = gspread.authorize(credentials)
sheet = gc.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# ---- CoinGecko API Setup ----
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 6,  # track top 6
    "page": 1,
    "price_change_percentage": "24h"
}
response = requests.get(url, params=params)
coins = response.json()

# ---- Format and Append Data ----
for coin in coins:
    row = [
        coin["name"],
        coin["symbol"].upper(),
        f'{coin["price_change_percentage_24h"]:.2f}%',
        f'₹{coin["current_price"]}',
        f'₹{coin["market_cap"]:,}',
        f'₹{coin["total_volume"]:,}',
        coin["market_cap_rank"],
        datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
    ]
    sheet.append_row(row, value_input_option="USER_ENTERED")

print("✅ Crypto data appended successfully.")