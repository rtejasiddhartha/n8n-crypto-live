import json
import gspread
import requests
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Load credentials from the local creds.json file
with open("creds.json") as f:
    service_account_info = json.load(f)

# Setup Google Sheets client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# Google Sheet and worksheet
sheet = gc.open_by_key("1Yc1DidfDwlaLDT3rpAnEJII4Y1vbrfTe5Ub4ZEUylsg")
worksheet = sheet.worksheet("Crypto-workflow")

# Fetch CoinGecko INR data
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