# 🧠 CryptoPulse: GitHub Workflow Failure & Docker Resurrection

## 📌 Overview

This project started with the idea of building a 24/7 crypto automation system using **n8n**. The goal was simple but ambitious:

- Fetch **real-time crypto data** from the CoinGecko API
- Push it to **Google Sheets** for dashboarding
- Send alerts to **Telegram**
- Run automatically every **15 minutes** without fail

We explored multiple implementation strategies and learned key lessons about automation reliability.

---

## 🚀 Approaches Attempted

### ✅ 1. n8n (Terminal - `n8n start`, Port 5678)

- Used the `n8n start` CLI to run workflows.
- Used a cron node to trigger data fetch every 15 minutes.
- Integrated with Telegram + Google Sheets successfully.

#### ❌ Problems:
- Required terminal to remain open indefinitely.
- Any crash or accidental close stopped the automation.
- **No built-in retry or persistence.**
- Gaps in data were noticed due to unnoticed failures.

---

### ⚙️ 2. GitHub Actions Workflow (`update_crypto_sheet.py + YAML`)

- Shifted to GitHub Actions for scheduled automation.
- The idea was to run Python code using GitHub-hosted runners every 15 minutes.
- Python handled CoinGecko API fetch, Telegram alerts, and Google Sheets logging.

#### ❌ Problems:
- GitHub cron jobs **did not run consistently**.
- Many 15-minute intervals were **silently skipped**, even when the code was correct.
- Even during active hours, gaps were observed in output logs and Google Sheet entries.

---

### 📉 Data Inconsistency Analysis (GitHub Actions)

We analyzed the `Crypto-workflow` Google Sheet populated via GitHub Actions automation.

| Metric                          | Value                              |
|----------------------------------|-------------------------------------|
| 🔢 Total trigger groups analyzed | **36** (from 370 rows)             |
| ❗️Inconsistent triggers          | **36 instances**                   |
| 🕓 Longest delay                 | **92.98 minutes** (~1h 33m)        |
| ⏱️ Average delay (of all 36)     | **30.79 minutes**                  |

> These 36 cases represent times where GitHub **missed the expected 15-minute trigger**. Even a 16- or 22-minute gap means a failure.

> This clearly shows that **GitHub Actions is unreliable** for high-frequency automation, especially when real-time dashboards depend on consistent intervals.

---

### 🐳 3. Dockerized n8n (Port 5679)

- Final shift was to run n8n using **Docker**, hosted locally.
- Docker container mapped to port `5679`, persistent volume enabled.
- Secrets and tokens were set as environment variables securely.
- This version **ran continuously**, even without an open terminal.

#### ✅ Benefits:
- **Runs in background** without requiring open terminal.
- **Triggers fired consistently every 15 minutes** (00, 15, 30, 45).
- **No missed intervals or hidden failures.**
- Best choice for 24/7 automation where data integrity is crucial.

---

## 📊 Final Verdict: What Worked Best?

| Method        | Reliability | Cost         | Setup Effort | Best Use Case              |
|---------------|-------------|--------------|--------------|----------------------------|
| `n8n start`   | ❌ Low      | Free         | Low          | Testing & Local Trials     |
| GitHub Action | ⚠️ Medium  | Free         | Medium       | Non-critical automation    |
| Docker n8n    | ✅ High     | Free (Local) | Medium       | **Reliable 24/7 Automation** |

---

## 📁 Repository Contents

| File                    | Description                                |
|-------------------------|--------------------------------------------|
| `update_crypto_sheet.py`| Main script that fetches, formats, sends data |
| `crypto-update.yml`     | GitHub Actions workflow file                |
| `requirements.txt`      | Python dependencies                        |
| `README.md`             | This file you're reading                    |

---

## 📸 Screenshots & Visuals

- ![n8n Workflow Screenshot](n8n_workflow.png)

---

## 📚 Lessons Learned

- **Don't rely on GitHub Actions for frequent scheduling**.
- Use Dockerized automation for background jobs with guaranteed runtime.
- Even simple cron-based triggers can silently fail without a proper watchdog system.
- Local Docker + n8n is a free and powerful alternative for serious automation users.

---

## 🔮 Next Steps

- Build **Looker Studio Dashboard** using Google Sheets logs.
- Add advanced analytics:
  - ATH proximity alerts
  - Volume anomaly spikes
  - Trend reversal detection
- Explore **wallet sync & portfolio tracking** for long-term monitoring.

---

## 📬 Author

> Maintained by [@rtejasiddhartha](https://github.com/rtejasiddhartha/)  
> Say hi on Telegram [@hamada5811] or [LinkedIn](https://www.linkedin.com/in/rtejasiddhartha/)

---
