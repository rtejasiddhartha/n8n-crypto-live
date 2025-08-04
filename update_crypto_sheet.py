import os
import json
import gspread
import requests
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

# Format INR numbers
def format_inr(value):
    try:
        return f"₹{int(value):,}"
    except:
        return "N/A"

# Trend labeling
def label_trend(pct):
    if pct > 0.05:
        return "🚀", "Bullish 🔥"
    elif pct < -0.05:
        return "🧊", "Bearish ❄️"
    else:
        return "⚖️", "Sideways ⚖️"

# Placeholder insight logic (can be improved with ATH data later)
def dummy_ath_insight(change):
    if change > 0.05:
        return "🟢 Near ATH"
    elif change > -0.05:
        return "🟡 Watch Zone"
    else:
        return "🔴 Far Below ATH"

# Placeholder range logic
def dummy_range(change):
    if change > 0.04:
        return "🔼 Near 24h High (100.0%)"
    elif change > -0.04:
        return "⚖️ In the Middle (76.3%)"
    else:
        return "🔽 Near 24h Low (20.0%)"

# Placeholder volatility logic
def dummy_volatility(change):
    if abs(change) > 5:
        return "🔥 High Volatility"
    elif abs(change) > 2:
        return "🟦 Medium Volatility"
    else:
        return "🟩 Low Volatility"

# Get IST time
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

# Get 50 coins
response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "price_change_percentage": "24h"
})
coins = response.json()
now_ist = get_ist_time()

# Grouped lists
bullish = []
sideways = []
bearish = []

# Process coins
for coin in coins:
    pct = coin.get("price_change_percentage_24h") or 0.0
    emoji, trend_text = label_trend(pct)
    row = [
        coin.get("name"),                           # Coin
        coin.get("symbol").upper(),                # Symbol
        emoji,                                      # Trend Emoji
        trend_text,                                 # Trend Text
        f"{pct:.4f}",                               # 24h Change
        format_inr(coin.get("current_price")),      # Current Price
        format_inr(coin.get("market_cap")),         # Market Cap
        format_inr(coin.get("total_volume")),       # 24h Volume
        coin.get("market_cap_rank"),                # Global Rank
        dummy_ath_insight(pct),                     # ATH Insight
        dummy_range(pct),                           # 24h Range
        dummy_volatility(pct),                      # Volatility
        f"https://www.coingecko.com/en/coins/{coin.get('id')}",  # Chart Link
        now_ist                                     # Updated At
    ]
    
    # Limit to 5 per category
    if emoji == "🚀" and len(bullish) < 5:
        bullish.append(row)
    elif emoji == "⚖️" and len(sideways) < 5:
        sideways.append(row)
    elif emoji == "🧊" and len(bearish) < 5:
        bearish.append(row)

# Final sorted list
rows_sorted = bullish + sideways + bearish

# Append to sheet (no headers)
worksheet.append_rows(rows_sorted)
