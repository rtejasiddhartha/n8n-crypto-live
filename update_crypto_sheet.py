import os
import json
import gspread
import requests
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

# INR formatter (international commas)
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

# IST timestamp
def get_ist_time():
    return (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")

# Auth
service_account_info = json.loads(os.environ["GCP_CREDENTIALS"])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# Google Sheet
sheet = gc.open_by_key("1Yc1DidfDwlaLDT3rpAnEJII4Y1vbrfTe5Ub4ZEUylsg")
worksheet = sheet.worksheet("Crypto-workflow")

# Fetch 50 coins
response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "price_change_percentage": "24h"
})
coins = response.json()

# Time
now_ist = get_ist_time()

# Top 5 sets
top_gainers = sorted(coins, key=lambda x: x['price_change_percentage_24h'] or 0, reverse=True)[:5]
top_losers = sorted(coins, key=lambda x: x['price_change_percentage_24h'] or 0)[:5]
top_volume = sorted(coins, key=lambda x: x['total_volume'], reverse=True)[:5]
top_market_cap = sorted(coins, key=lambda x: x['market_cap'], reverse=True)[:5]

# Unique coins
top_combined = {coin['id']: coin for coin in top_gainers + top_losers + top_volume + top_market_cap}

# Format data
rows = []
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

    rows.append([
        name, symbol, f"{change:.4f}", price, market_cap, volume,
        rank, trend_label, chart_link, now_ist
    ])

# Sort by Trend order: Bullish > Sideways > Bearish
trend_order = {"🚀 Bullish": 1, "⚖️ Sideways": 2, "🧊 Bearish": 3}
rows_sorted = sorted(rows, key=lambda x: trend_order.get(x[7], 99))

# Write to sheet
headers = [
    "Coin", "Symbol", "24h Change (%)", "Current Price", "Market Cap",
    "24h Volume", "Global Rank", "Trend", "Chart Link", "Updated At"
]
worksheet.clear()
worksheet.append_row(headers)
worksheet.append_rows(rows_sorted)
