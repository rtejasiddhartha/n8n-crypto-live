import os
import json
import gspread
import requests
import time
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

def log_trigger_to_sheet(trigger_type="schedule", status="✅ Success"):
    try:
        utc_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        ist_now = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
        log_row = [utc_now, ist_now, trigger_type, status]

        log_ws = gc.open_by_key("1Yc1DidfDwlaLDT3rpAnEJII4Y1vbrfTe5Ub4ZEUylsg").worksheet("Trigger-Logs")
        log_ws.append_row(log_row)
        print(f"✅ Logged trigger to sheet at {ist_now}")
    except Exception as e:
        print("❌ Failed to log trigger:", e)
        
# Align to 00,15,30,45 before proceeding
def wait_until_next_slot():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    next_minute = ((now.minute // 15) + 1) * 15
    if next_minute == 60:
        next_slot = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        next_slot = now.replace(minute=next_minute, second=0, microsecond=0)
    wait_sec = (next_slot - now).total_seconds()
    if 0 < wait_sec < 60:
        print(f"⏳ Waiting {int(wait_sec)} seconds to sync at {next_slot.strftime('%H:%M')} IST...")
        time.sleep(wait_sec)

wait_until_next_slot()

# INR formatter
def format_inr(value):
    try:
        return f"₹{int(value):,}"
    except:
        return "N/A"

# Trend classifier
def label_trend(pct):
    if pct > 0.05:
        return "🚀", "Bullish 🔥"
    elif pct < -0.05:
        return "🧊", "Bearish ❄️"
    else:
        return "⚖️", "Sideways ⚖️"

# ATH Insight (placeholder)
def dummy_ath_insight(change):
    if change > 0.05:
        return "🟢 Near ATH"
    elif change > -0.05:
        return "🟡 Watch Zone"
    else:
        return "🔴 Far Below ATH"

# 24h Range
def dummy_range(change):
    if change > 0.04:
        return "🔼 Near 24h High (100.0%)"
    elif change > -0.04:
        return "⚖️ In the Middle (76.3%)"
    else:
        return "🔽 Near 24h Low (20.0%)"

# Volatility marker
def dummy_volatility(change):
    if abs(change) > 5:
        return "🔥 High Volatility"
    elif abs(change) > 2:
        return "🟦 Medium Volatility"
    else:
        return "🟩 Low Volatility"

# IST time
def get_ist_time():
    return (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%-d/%-m/%Y, %-I:%M:%S %p")

# Telegram alert for each coin
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
📅 Updated: {updated}"""

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    response = requests.post(url, data=payload)
    print(f"📤 Telegram: {name} – {response.status_code}")

# GSheet auth
service_account_info = json.loads(os.environ["GCP_CREDENTIALS"])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# Google Sheet
sheet = gc.open_by_key("1Yc1DidfDwlaLDT3rpAnEJII4Y1vbrfTe5Ub4ZEUylsg")
worksheet = sheet.worksheet("Crypto-workflow")

# Fetch CoinGecko data
response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "price_change_percentage": "24h"
})
coins = response.json()
now_ist = get_ist_time()

# Process data
bullish, sideways, bearish = [], [], []

for coin in coins:
    pct = coin.get("price_change_percentage_24h") or 0.0
    emoji, trend_text = label_trend(pct)

    row = [
        coin.get("name"),
        coin.get("symbol").upper(),
        emoji,
        trend_text,
        f"{pct:.2f}%",
        format_inr(coin.get("current_price")),
        format_inr(coin.get("market_cap")),
        format_inr(coin.get("total_volume")),
        coin.get("market_cap_rank"),
        dummy_ath_insight(pct),
        dummy_range(pct),
        dummy_volatility(pct),
        f"https://www.coingecko.com/en/coins/{coin.get('id')}",
        now_ist
    ]

    if emoji == "🚀" and len(bullish) < 5:
        bullish.append(row)
    elif emoji == "⚖️" and len(sideways) < 5:
        sideways.append(row)
    elif emoji == "🧊" and len(bearish) < 5:
        bearish.append(row)

# Final sort + log
rows_sorted = bullish + sideways + bearish
worksheet.append_rows(rows_sorted)

# Send alerts
for coin in rows_sorted:
    send_telegram_alert(coin)

print(f"✅ Completed: {len(rows_sorted)} coins sent and logged at {now_ist}")
