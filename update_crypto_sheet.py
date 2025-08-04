import os
import json
import gspread
import requests
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

# INR format
def format_inr(value):
    try:
        return f"₹{int(value):,}"
    except:
        return "N/A"

# Trend classification
def label_trend(pct):
    if pct > 0.05:
        return "🚀", "Bullish 🔥"
    elif pct < -0.05:
        return "🧊", "Bearish ❄️"
    else:
        return "⚖️", "Sideways ⚖️"

def dummy_ath_insight(change):
    if change > 0.05:
        return "🟢 Near ATH"
    elif change > -0.05:
        return "🟡 Watch Zone"
    else:
        return "🔴 Far Below ATH"

def dummy_range(change):
    if change > 0.04:
        return "🔼 Near 24h High (100.0%)"
    elif change > -0.04:
        return "⚖️ In the Middle (76.3%)"
    else:
        return "🔽 Near 24h Low (20.0%)"

def dummy_volatility(change):
    if abs(change) > 5:
        return "🔥 High Volatility"
    elif abs(change) > 2:
        return "🟦 Medium Volatility"
    else:
        return "🟩 Low Volatility"

def get_ist_time():
    return (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%-d/%-m/%Y, %-I:%M %p")

# Telegram alert per coin
def send_telegram_alert(coin):
    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = "@cryptopulsebot_in"
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

    emoji = coin[2]
    name = coin[0]
    symbol = coin[1]
    trend = coin[3]
    change = coin[4]
    price = coin[5]
    market_cap = coin[6]
    volume = coin[7] + " 🔻"
    rank = coin[8]
    ath = coin[9]
    range_ = coin[10]
    volatility = coin[11]
    chart = coin[12]
    updated = coin[13]

    message = f"""{emoji} <b>Crypto Alert: {name} ({symbol})</b>\n
<b>Trend:</b> {trend}  
<b>24h Change:</b> {change}  
<b>Current Price:</b> {price}  
<b>Market Cap:</b> {market_cap}  
<b>24h Volume:</b> {volume}  
<b>Global Rank:</b> {rank}\n
<b>ATH Insight:</b> {ath}  
<b>24h Range:</b> {range_}  
<b>Volatility:</b> {volatility}\n
📊 <a href="{chart}">View Chart</a>  
📅 Updated: {updated}  
📈 Data Source: CoinGecko (INR)  
🔁 Triggered by: GitHub + Python"""

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True  # 👈 disables that CoinGecko box preview
    }

    response = requests.post(url, data=payload)
    print(f"Telegram: {name} – {response.status_code}")

# Auth
service_account_info = json.loads(os.environ["GCP_CREDENTIALS"])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# Open Sheet
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

# Group coins
bullish, sideways, bearish = [], [], []
rows_sorted = []

for coin in coins:
    pct = coin.get("price_change_percentage_24h") or 0.0
    emoji, trend_text = label_trend(pct)

    row = [
        coin.get("name"),                           # Coin
        coin.get("symbol").upper(),                # Symbol
        emoji,                                      # Trend Emoji
        trend_text,                                 # Trend Text
        f"{pct:.2f}%",                              # 24h Change
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

    if emoji == "🚀" and len(bullish) < 5:
        bullish.append(row)
    elif emoji == "⚖️" and len(sideways) < 5:
        sideways.append(row)
    elif emoji == "🧊" and len(bearish) < 5:
        bearish.append(row)

# Combine and send
rows_sorted = bullish + sideways + bearish
worksheet.append_rows(rows_sorted)

for coin in rows_sorted:
    send_telegram_alert(coin)
