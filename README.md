# CryptoLens AI — End-to-End Crypto Analytics (BI + AI)

CryptoLens AI is a **personal analytics project** that demonstrates how raw crypto
market data can be transformed into **interactive business dashboards** and
**AI-assisted market insights** using modern analytics and cloud tooling.

The project is built incrementally, following a **realistic analytics lifecycle**
—from ingestion to reporting to AI—while consciously balancing **scope, cost,
and engineering trade-offs**.

---

## What This Project Demonstrates

- Automated crypto data ingestion
- Data cleaning and preparation
- Cloud data warehousing
- Analytical modeling (facts & dimensions)
- Business intelligence dashboards
- AI-assisted market commentary
- Lightweight application deployment

---

## Project Evolution (What Was Actually Built)

### Phase 0 — Data Ingestion (n8n)
- Implemented crypto market ingestion using **n8n**
- Focused on reliability, retries, and real-world data imperfections
- Established raw data pipelines for downstream analytics

### Phase 1 — Data Preparation
- Cleaned and normalized raw crypto data
- Handled missing values and inconsistent records
- Produced a stable dataset (`crypto_cleaned_v1.csv`) for analytics

### Phase 2 — Cloud Warehouse (BigQuery)
- Loaded cleaned data into **BigQuery**
- Designed **fact and dimension tables**
- Structured schema for analytical and BI workloads

### Phase 3 — Business Intelligence (Power BI)
- Connected Power BI directly to BigQuery
- Built multi-page dashboards:
  - Market overview
  - Coin-level metrics
  - ATH proximity analysis
  - Momentum trends
- Dashboards reflect real analytical transformations, not static mock data

### Phase 4 — Application Layer (Streamlit)
- Embedded Power BI dashboards inside **Streamlit**
- Created a single interface for analytics + insights
- Kept frontend simple and analytics-focused

### Phase 5 — AI-Assisted Insights (Gemini)
- Integrated **Gemini AI** to generate:
  - Market summaries
  - Momentum explanations
  - ATH risk context
- Insights are:
  - Observational only
  - Based on dashboard-level aggregates
  - Rate-limited to control API usage and cost

> Live AI generation on every dashboard interaction was intentionally avoided.
> This project prioritizes **architecture clarity and cost awareness** over
> high-frequency AI calls.

---

## Current Status

- ✅ Ingestion → Cleaning → Warehouse → BI → AI insights fully connected
- ✅ Deployed using Streamlit Cloud
- ✅ Gemini insights working with controlled usage
- ❌ Real-time AI per slicer interaction (by design)

---

## Repository Structure (Simplified)

n8n-crypto-live/
│ (n8n workflows)
│
├── 00_foundation_crypto_ingestion/ # Ingestion & reliability
├── 01_data_preparation/ # Cleaning & validation
├── ai_insights_layer_02/ # Gemini insight logic
├── streamlit_app_03/ # Streamlit application
├── requirements.txt
└── README.md


---

## Design Principles

- **Realistic data**: Raw data is intentionally imperfect
- **Explainability**: Metrics and insights are transparent and traceable
- **Free-tier first**: Tools chosen with cost awareness
- **Progressive build**: Each phase builds on the previous one
- **No hype**: Observations over predictions, analytics over speculation

---

## Final Note

CryptoLens AI is not a trading system.

It is a **documented analytics journey** showing how raw data becomes
dashboards and how dashboards can be translated into **clear, AI-assisted
market insights**—built the way real analytics platforms evolve.
