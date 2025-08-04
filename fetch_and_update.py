import os
import json
import requests
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# ---- Authorize Google Sheets with ENV ----
service_account_info = json.loads(os.environ["GCP_CREDENTIALS"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# ---- Sheet Config ----
SHEET_ID = "1Yc1DidfDwlaLDT3rpAnEJII4Y1vbrfTe5Ub4ZEUylsg"
WORKSHEET_NAME = "CryptoPulseAlerts"
worksheet = gc.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)

# ---- Fetch Data from CoinGecko ----
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 6,
    "page": 1,
    "price_change_percentage": "24h"
}
response = requests.get(url, params=params)
coins = response.json()

# ---- Format and Append Each Row ----
for coin in coins:
    # 24h Change %
    change_24h = coin["price_change_percentage_24h"]
    trend = "Bullish 🔥" if change_24h >= 5 else "Bearish ❄️" if change_24h <= -5 else "Sideways ⚖️"
    trend_emoji = "🚀" if change_24h >= 5 else "📉" if change_24h <= -5 else "⚖️"

    # Format fields
    price = f'₹{coin["current_price"]:,}'
    change_str = f'{change_24h:+.2f}%'
    market_cap = f'₹{coin["market_cap"]:,}'
    volume = f'₹{coin["total_volume"]:,}'
    rank = f'#{coin["market_cap_rank"]}'
    chart_link = f'https://www.coingecko.com/en/coins/{coin["id"]}'
    updated_at = datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")

    # ATH Insight
    ath_distance = ((coin["ath"] - coin["current_price"]) / coin["ath"]) * 100
    ath_label = (
        "🟢 Near ATH" if ath_distance < 10 else
        "🟡 Watch Zone" if ath_distance < 25 else
        "🔴 Far Below ATH"
    )

    # 24h Range
    high = coin["high_24h"]
    low = coin["low_24h"]
    range_percent = ((coin["current_price"] - low) / (high - low)) * 100 if (high - low) != 0 else 0
    range_label = (
        f'🔼 Near 24h High ({range_percent:.1f}%)' if range_percent >= 80 else
        f'🔽 Near 24h Low ({range_percent:.1f}%)' if range_percent <= 20 else
        f'⚖️ In the Middle ({range_percent:.1f}%)'
    )

    # Volatility
    volatility_score = ((high - low) / coin["current_price"]) * 100 if coin["current_price"] else 0
    volatility = (
        "🔥 High Volatility" if volatility_score > 10 else
        "🟦 Medium Volatility" if volatility_score > 5 else
        "🟩 Low Volatility"
    )

    # Row Mapping (Matches Google Sheets columns)
    row = [
        coin["name"],                       # Coin
        coin["symbol"].upper(),            # Symbol
        trend,                             # Trend
        change_str,                        # 24h Change
        price,                             # Current Price
        market_cap,                        # Market Cap
        volume,                            # 24h Volume
        rank,                              # Global Rank
        ath_label,                         # ATH Insight
        range_label,                       # 24h Range
        volatility,                        # Volatility
        chart_link,                        # Chart Link
        updated_at,                        # Updated At
        trend_emoji                        # Trend Emoji
    ]

    worksheet.append_row(row, value_input_option="USER_ENTERED")

print("✅ All crypto rows appended to Google Sheets.")