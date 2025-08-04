import os
import json
import gspread
import requests
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import locale

# Set INR formatting
def format_inr(value):
    try:
        # Manual INR-style formatting: 1,23,45,678
        s = f"{int(value):,}"
        parts = s.split(",")
        if len(parts) <= 2:
            return f"₹{s}"
        return f"₹{parts[0]},{''.join(parts[1:-1])},{parts[-1]}"
    except:
        return "N/A"

# Label trend
def label_trend(pct):
    if pct > 0.05:
        return "🚀 Bullish"
    elif pct < -0.05:
        return "🧊 Bearish"
    else:
        return "⚖️ Sideways"

# Auth with GCP credentials
service_account_info = json.loads(os.environ["GCP_CREDENTIALS"])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# Open Google Sheet
sheet = gc.open_by_key("1Yc1DidfDwlaLDT3rpAnEJII4Y1vbrfTe5Ub4ZEUylsg")
worksheet = sheet.worksheet("Crypto-workflow")

# Fetch top 50 coins
response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "price_change_percentage": "24h"
})
coins = response.json()

# Format records
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
formatted_rows = []

# Sort logic for top categories
top_gainers = sorted(coins, key=lambda x: x['price_change_percentage_24h'] or 0, reverse=True)[:5]
top_losers = sorted(coins, key=lambda x: x['price_change_percentage_24h'] or 0)[:5]
top_volume = sorted(coins, key=lambda x: x['total_volume'], reverse=True)[:5]
top_market_cap = sorted(coins, key=lambda x: x['market_cap'], reverse=True)[:5]

# Merge all unique coins from these top sets
top_combined = {coin['id']: coin for coin in top_gainers + top_losers + top_volume + top_market_cap}

for coin in top_combined.values():
    name = coin.get("name")
    symbol = coin.get("symbol").upper()
    price = format_inr(coin.get("current_price"))
    change = coin.get("price_change_percentage_24h") or 0.0
    market_cap = format_inr(coin.get("market_cap"))
    volume = format_inr(coin.get("total_volume"))
    rank = coin.get("market_cap_rank")
    chart_link = f"https://www.coingecko.com/en/coins/{coin.get('id')}"
    trend_label = label_trend(change)

    formatted_rows.append([
        name, symbol, f"{change:.4f}", price, market_cap, volume,
        rank, trend_label, chart_link, now
    ])

# Push to sheet (replace or append)
headers = [
    "Coin", "Symbol", "24h Change (%)", "Current Price", "Market Cap",
    "24h Volume", "Global Rank", "Trend", "Chart Link", "Updated At"
]
worksheet.clear()
worksheet.append_row(headers)
worksheet.append_rows(formatted_rows)
