import os
import json
import gspread
import requests
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

# INR formatter
def format_inr(value):
    try:
        return f"₹{int(value):,}"
    except:
        return "N/A"

# Trend label
def label_trend(pct):
    if pct > 0.05:
        return "🚀 Bullish"
    elif pct < -0.05:
        return "🧊 Bearish"
    else:
        return "⚖️ Sideways"

# IST time
def get_ist_time():
    return (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")

# Auth
service_account_info = json.loads(os.environ["GCP_CREDENTIALS"])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# Sheet
sheet = gc.open_by_key("1Yc1DidfDwlaLDT3rpAnEJII4Y1vbrfTe5Ub4ZEUylsg")
worksheet = sheet.worksheet("Crypto-workflow")

# Fetch coins
response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "price_change_percentage": "24h"
})
coins = response.json()
now_ist = get_ist_time()

# Sort coins by trend categories
bullish = []
sideways = []
bearish = []

for coin in coins:
    pct = coin.get("price_change_percentage_24h") or 0.0
    trend = label_trend(pct)
    entry = [
        coin.get("name"),
        coin.get("symbol").upper(),
        f"{pct:.4f}",
        format_inr(coin.get("current_price")),
        format_inr(coin.get("market_cap")),
        format_inr(coin.get("total_volume")),
        coin.get("market_cap_rank"),
        trend,
        f"https://www.coingecko.com/en/coins/{coin.get('id')}",
        now_ist
    ]
    if trend == "🚀 Bullish" and len(bullish) < 5:
        bullish.append(entry)
    elif trend == "⚖️ Sideways" and len(sideways) < 5:
        sideways.append(entry)
    elif trend == "🧊 Bearish" and len(bearish) < 5:
        bearish.append(entry)

# Combine all rows: Bullish > Sideways > Bearish
rows_sorted = bullish + sideways + bearish

# Append rows (no headers)
worksheet.append_rows(rows_sorted)
