# 🧠 CryptoPulse: GitHub Workflow-Based Crypto Automation (Failed Attempt)

## 📌 Overview

This project was an experimental attempt to automate a **15-minute interval crypto monitoring system** using:

- **CoinGecko API** – to fetch live top coin data
- **Google Sheets** – to log every cycle for dashboard use
- **Telegram Bot** – to send alerts with trend, volume, and volatility
- **GitHub Actions** – to trigger the automation every 15 minutes

---

## 🎯 Objective

Build a low-cost, GitHub-powered crypto bot that could:
- Run every 15 minutes (00, 15, 30, 45)
- Log data consistently into Google Sheets
- Alert via Telegram with live insights
- Act as a backend engine for real-time dashboards

---

## ⚙️ Architecture

- `update_crypto_sheet.py` handles:
  - API calls to CoinGecko
  - Data formatting
  - Google Sheets logging
  - Telegram alerting
- `crypto-update.yml` defines:
  - Schedule: Every 15 minutes via cron
  - Secrets: `GCP_CREDENTIALS` and `TELEGRAM_BOT_TOKEN`
  - Execution steps with Python environment

---

## 📉 Data Inconsistency Analysis (GitHub Actions Approach)

We analyzed the **`Crypto-workflow` Google Sheet**, which logged 370 entries using GitHub-scheduled Python automation.

| Metric                          | Value                              |
|----------------------------------|-------------------------------------|
| 🔢 Total trigger groups analyzed | **36** (from 370 rows)             |
| ❗️Inconsistent triggers          | **36 instances**                   |
| 🕓 Longest delay                 | **92.98 minutes** (~1h 33m)        |
| ⏱️ Average delay (of all 36)     | **30.79 minutes**                  |

> These 36 instances represent cases where the expected 15-minute execution **did not occur on time** — even a 16-minute or 22-minute gap indicates missed triggers.

> This confirms that **GitHub Actions cron jobs are not suitable for high-frequency or real-time automation**, especially when precise execution windows are required for analytics dashboards.

---

## 📂 Repository Contents

| File                    | Description                                |
|-------------------------|--------------------------------------------|
| `update_crypto_sheet.py`| Python script that powers the workflow     |
| `crypto-update.yml`     | GitHub Actions workflow definition         |
| `requirements.txt`      | All dependencies used                      |

---

## ❌ Why This Approach Failed

- **Unreliable Schedule**: GitHub's runners are not optimized for consistent interval-based jobs (like every 15 minutes).
- **No Real Guarantee**: Even with correct cron syntax (`0,15,30,45 * * * *`), the job may not execute as expected due to:
  - Runner availability
  - Cold starts
  - Global runner limitations
- **Invisible Failures**: Triggers silently skipped without logging errors
- **Result**: Gaps in time-series data → inaccurate dashboards

---

## 📊 What Did Work?

- Python script executed perfectly when run manually or locally
- Telegram alerts worked with rich formatting
- Google Sheets integration was smooth and append-only
- The system works perfectly **if trigger execution is guaranteed exactly in 15 minutes everytime**

---

## 🐳 Future Solution → Dockerized n8n

After this failed approach, the project was shifted to **n8n running inside Docker**, which:
- Uses persistent workflows
- Supports webhook triggers, CRONs, and retries
- Doesn’t stop even when terminal closes
- Offers more reliability for 24/7 systems
---

## 📚 Lessons Learned

- GitHub Actions are **not suitable for real-time analytics bots**
- For anything below 1-hour frequency, use **Docker, Cron on a VM, or Replit/GCP Functions**
- Always analyze logs & results — automation can silently fail
- Data integrity matters for time-sensitive dashboards

---

## 🔮 What’s Next?

- Finalize the new Docker-hosted n8n automation
- Build a **Looker Studio** dashboard on top of Google Sheets
- Extend alerts with:
  - ATH insights
  - Volume anomaly detection
  - Trend reversals (3h, 6h)
- Integrate CoinMarketCap & Twitter API for sentiment + price prediction

---

## 📬 Author

> Maintained by [@rtejasiddhartha](https://github.com/rtejasiddhartha/)  
> Say hi on Telegram [@hamada5811] or [LinkedIn](https://www.linkedin.com/in/rtejasiddhartha/)

---
