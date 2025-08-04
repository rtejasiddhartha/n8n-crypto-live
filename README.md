# 🚀 CryptoPulse Alerts

Real-Time Cryptocurrency Analytics & Alerting System  
Built using **n8n (for prototyping)** and **GitHub Actions + Python (for production)**

---

## 📌 Project Summary

**CryptoPulse Alerts** is a live crypto tracking and alert system that:

- Fetches real-time INR-based data from the **CoinGecko API**
- Categorizes top 50 coins into:
  - 🚀 Bullish  
  - ⚖️ Sideways  
  - 🧊 Bearish  
- Logs the top 15 (5 per category) to **Google Sheets**
- Sends **Telegram alerts** every 15 minutes
- Powers a **Google Looker Studio dashboard** for interactive analysis

---

## 🎯 Key Features

| Feature                       | Tech Used                         |
|------------------------------|-----------------------------------|
| 🔁 Automation Engine          | GitHub Actions (cron every 15 min)|
| 🔧 Visual Workflow Prototyping| n8n 2025+                         |
| 🧠 Market Data                | CoinGecko API                     |
| 📊 Storage                   | Google Sheets via Service Account |
| 📈 Dashboarding               | Google Looker Studio              |
| 📣 Alerts                    | Telegram Bot API (HTML mode)     |
| 💰 Cost                      | 💯 100% Free Tier Only            |

---

## 🧠 Why n8n + GitHub?

This project was first **designed in n8n** to build a visual, low-code pipeline.  
However, due to limitations in free-tier Docker-based hosting for 24/7 workflows,  
the logic was **migrated to Python + GitHub Actions** for reliable, cost-free automation.

The GitHub version runs a Python script every 15 minutes using cron,  
pushing formatted coin data to Google Sheets and sending styled Telegram alerts.

> ✅ The final system is production-ready and runs 100% free — with dashboards and alerts in real-time.

---

## 🛠️ How It Works

1. **`update_crypto_sheet.py`**:
   - Fetches top 50 INR coins from CoinGecko
   - Categorizes coins (Bullish, Sideways, Bearish)
   - Formats INR values, emojis, and insight labels
   - Logs structured rows to Google Sheets
   - Sends one message per coin to Telegram using HTML formatting

2. **`.github/workflows/crypto_alert.yml`**:
   - Runs the script every 15 minutes using GitHub Actions
   - Loads secrets from GitHub (Telegram token, GCP credentials)
   - Requires no servers, no cron jobs, no Docker

---

## 📂 Repo Structure

```
.
├── update_crypto_sheet.py         # Main script
├── .github/
│   └── workflows/
│       └── crypto_alert.yml       # GitHub Action (cron trigger)
├── assets/
│   └── n8n_workflow.png           # Screenshot of original n8n design
├── README.md                      # This file
```

---

## 📊 Dashboard Preview

📈 **Google Looker Studio Dashboard (Live)**  
🔗 [Coming Soon – Public Link]

---

## 📲 Telegram Channel

Join the real-time alert feed:  
🔗 [@cryptopulsebot_in](https://t.me/cryptopulsebot_in)

---

## 🔐 Environment Variables Required (Secrets)

| Key                  | Purpose                          |
|----------------------|----------------------------------|
| `GCP_CREDENTIALS`    | Google Sheets service account JSON |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot token for alerts     |

These must be added as **GitHub Secrets** for the Actions workflow to function.

---

## 🧠 Future Improvements

- Add **ATH detection using real ATH price**
- Detect **3h/6h trend reversals**
- Add **volume spikes + anomaly alerts**
- Enhance **Looker Studio dashboard** with trend filters and emoji KPIs
- Add **historical sheet logging** for charting

---

## 💼 Project Type

- ✅ **Data Analyst Project**
- ✅ **API Integration**
- ✅ **Real-Time Alerting**
- ✅ **Serverless Automation**
- ✅ **Portfolio & Resume Showcase Ready**

---

## 🧑‍💻 Built With

- `Python 3.11`
- `gspread`, `oauth2client`, `requests`
- `GitHub Actions`
- `Google Sheets + Looker Studio`
- `Telegram Bot API`
- `n8n 2025+` (for initial design)

---

## 📬 Author

> Maintained by [@yourgithub](https://github.com/yourgithub)  
> Say hi on Telegram [@yourhandle] or [LinkedIn](https://linkedin.com/in/yourprofile)

---
