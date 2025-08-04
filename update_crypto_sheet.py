import os
import json
import gspread
import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+ for timezones
from oauth2client.service_account import ServiceAccountCredentials

# ---- Google Sheets Authorization using GCP_CREDENTIALS from ENV ----
service_account_info = json.loads(os.environ["GCP_CREDENTIALS"])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# ---- Open Google Sheet ----
sheet = gc.open_by_key("1Yc1DidfDwlaLDT3rpAnEJII4Y1vbrfTe5Ub4ZEUylsg")
worksheet = sheet.worksheet("Crypto-workflow")

# ---- Fetch top 10 INR coins from CoinGecko ----
response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "price_change_percentage": "24h"
})
coins = response.json()

# ---- Format and append each row to sheet ----
for coin in coins:
    price = coin["current_price"]
    high = coin["high_24h"]
    low = coin["low_24h"]

    # Trend and Emoji
    change_pct = coin["price_change_percentage_24h"]
    trend = "Bullish 🔥" if change_pct > 5 else "Bearish ❄️" if change_pct < -5 else "Sideways ⚖️"
    emoji = "🚀" if "Bullish" in trend else "📉" if "Bearish" in trend else "⚖️"

    # ATH insight
    ath_diff = ((coin["ath"] - price) / coin["ath"]) * 100 if coin["ath"] else 0
    ath_label = "🟢 Near ATH" if ath_diff < 10 else "🟡 Watch Zone" if ath_diff < 25 else "🔴 Far Below ATH"

    # 24h range insight
    range_pos = ((price - low) / (high - low)) * 100 if high != low else 0
    range_label = (
        "🔼 Near 24h High" if range_pos >= 80 else
        "🔽 Near 24h Low" if range_pos <= 20 else
        "⚖️ In the Middle"
    )
    range_str = f"{range_label} ({range_pos:.1f}%)"

    # Volatility
    volatility = ((high - low) / price) * 100 if price else 0
    volatility_badge = (
        "🔥 High Volatility" if volatility > 10 else
        "🟦 Medium Volatility" if volatility > 5 else
        "🟩 Low Volatility"
    )

    # Append row to sheet
    worksheet.append_row([
        coin["name"],                                 # Coin
        coin["symbol"].upper(),                       # Symbol
        emoji,                                        # Trend Emoji
        trend,                                        # Trend
        f"{change_pct:.2f}%",                         # 24h Change
        f"₹{price:,}",                                # Current Price
        f"₹{coin['market_cap']:,}",                   # Market Cap
        f"₹{coin['total_volume']:,}",                 # 24h Volume
        coin["market_cap_rank"],                      # Global Rank
        ath_label,                                    # ATH Insight
        range_str,                                    # 24h Range
        volatility_badge,                             # Volatility
        f"https://www.coingecko.com/en/coins/{coin['id']}",  # Chart Link
        datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")  # IST timestamp
    ], value_input_option="USER_ENTERED")

print("✅ update_crypto_sheet.py completed and rows appended to Google Sheets.")