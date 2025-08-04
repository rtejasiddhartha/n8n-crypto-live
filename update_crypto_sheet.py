import os
import json
import gspread
import requests
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Authorize using GCP_CREDENTIALS environment variable
service_account_info = json.loads(os.environ["GCP_CREDENTIALS"])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# Open sheet
sheet = gc.open_by_key("1Yc1DidfDwlaLDT3rpAnEJII4Y1vbrfTe5Ub4ZEUylsg")
worksheet = sheet.worksheet("Crypto-workflow")

# Fetch top 10 INR coins
response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "price_change_percentage": "24h"
})
coins = response.json()

# Format and push each row to sheet
for coin in coins:
    high = coin["high_24h"]
    low = coin["low_24h"]
    price = coin["current_price"]

    ath_diff = ((coin["ath"] - price) / coin["ath"]) * 100
    ath_label = "🟢 Near ATH" if ath_diff < 10 else "🟡 Watch Zone" if ath_diff < 25 else "🔴 Far Below ATH"

    range_pos = ((price - low) / (high - low)) * 100 if high != low else 0
    range_label = "🔼 Near 24h High" if range_pos >= 80 else "🔽 Near 24h Low" if range_pos <= 20 else "⚖️ In the Middle"
    range_str = f"{range_label} ({range_pos:.1f}%)"

    volatility = ((high - low) / price) * 100 if price else 0
    volatility_badge = "🔥 High Volatility" if volatility > 10 else "🟦 Medium Volatility" if volatility > 5 else "🟩 Low Volatility"

    change = f"{coin['price_change_percentage_24h']:.2f}%"
    trend = "Bullish 🔥" if coin["price_change_percentage_24h"] > 5 else "Bearish ❄️" if coin["price_change_percentage_24h"] < -5 else "Sideways ⚖️"
    emoji = "🚀" if "Bullish" in trend else "📉" if "Bearish" in trend else "⚖️"

    worksheet.append_row([
        coin["name"],
        coin["symbol"].upper(),
        emoji,
        trend,
        change,
        f"₹{price}",
        f"₹{coin['market_cap']}",
        f"₹{coin['total_volume']}",
        f"{coin['market_cap_rank']}",
        ath_label,
        range_str,
        volatility_badge,
        f"https://www.coingecko.com/en/coins/{coin['id']}",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

    ], value_input_option="USER_ENTERED")