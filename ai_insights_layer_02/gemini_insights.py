"""
Gemini-Powered Market Insights
CryptoLens AI — Narrative Layer (FINAL)

Design goals:
- Short, report-style insights
- Strictly reflect dashboard values
- No predictions, no advice
- Low token usage
- Safe for public deployment
"""

import os
import time
from datetime import datetime
from typing import Dict

import streamlit as st
from google import genai

# ------------------------------------------------------------
# API KEY RESOLUTION (LOCAL + CLOUD SAFE)
# ------------------------------------------------------------

def get_api_key() -> str:
    # 1. Try Streamlit secrets (Cloud or local secrets.toml)
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass  # secrets.toml does not exist locally

    # 2. Fallback to environment variable (.env or OS)
    return os.getenv("GOOGLE_API_KEY")


API_KEY = get_api_key()

if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in environment or Streamlit secrets")

# ------------------------------------------------------------
# Gemini Client
# ------------------------------------------------------------

MODEL_NAME = "gemini-2.0-flash"

client = genai.Client(api_key=API_KEY)


# ---------------------------------------------------------
# 3. Dashboard Snapshot (DEFAULT VIEW)
# ---------------------------------------------------------

DASHBOARD_CONTEXT = {
    "coins": "ALL_COINS",
    "period": "17 Jul 2025 – 04 Oct 2025"
}


# ---------------------------------------------------------
# 4. Dashboard Values (MATCH POWER BI)
# ---------------------------------------------------------

def get_market_overview() -> Dict:
    return {
        "total_market_cap_trillion": 343.35,
        "avg_24h_change_pct": 0.29,
        "top_gainer_coin": "BNB",
        "top_gainer_pct": 0.05,
        "top_loser_coin": "XRP",
        "top_loser_pct": -0.01,
        "market_coverage_pct": 100,
        "period": DASHBOARD_CONTEXT["period"]
    }


def get_bitcoin_structure() -> Dict:
    return {
        "bitcoin_market_share_pct": 60.73
    }


def get_ath_distribution() -> Dict:
    return {
        "far_below_ath_pct": 58.46,
        "watch_zone_pct": 24.62,
        "near_ath_pct": 16.92
    }


def get_monthly_momentum() -> Dict:
    return {
        "July_2025":  {"Far Below": -3.57, "Watch": -3.17, "Near": -9.45},
        "August_2025":{"Far Below":  1.94, "Watch":  3.09, "Near":  0.75},
        "September_2025":{"Far Below": -1.24,"Watch": 0.18,"Near": -0.33},
        "October_2025":{"Far Below":  0.66,"Watch": 0.68,"Near": 4.84},
    }


# ---------------------------------------------------------
# 5. Prompt Builders (SHORT & CONTROLLED)
# ---------------------------------------------------------

def market_overview_prompt(data: Dict) -> str:
    return f"""
Dashboard snapshot (ALL coins):

- Market cap: ₹{data['total_market_cap_trillion']}T
- Avg 24h change: {data['avg_24h_change_pct']}%
- Top gainer: {data['top_gainer_coin']} ({data['top_gainer_pct']}%)
- Top loser: {data['top_loser_coin']} ({data['top_loser_pct']}%)
- Coverage: {data['market_coverage_pct']}%
- Period: {data['period']}

Write a concise market overview in 3–4 sentences.
No speculation. No advice.
"""


def bitcoin_structure_prompt(data: Dict) -> str:
    return f"""
Bitcoin dashboard view:

- Bitcoin market share: {data['bitcoin_market_share_pct']}%

Explain Bitcoin’s structural dominance in 1–2 sentences.
No forecasting.
"""


def momentum_prompt(data: Dict) -> str:
    return f"""
Monthly momentum by ATH category (%):

{data}

Summarize trends across months in short bullet points.
Focus on rotation and strength shifts.
"""


def risk_prompt(data: Dict) -> str:
    return f"""
ATH proximity distribution (%):

{data}

Explain market positioning in 3 short bullets.
Neutral, factual tone only.
"""


# ---------------------------------------------------------
# 6. Gemini Call (LOW TOKEN, SAFE)
# ---------------------------------------------------------

def call_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": 0.25,
            "max_output_tokens": 180
        }
    )
    time.sleep(0.4)
    return response.text.strip()


# ---------------------------------------------------------
# 7. Insight Orchestrator
# ---------------------------------------------------------

def generate_full_market_insight() -> Dict:
    return {
        "market_overview": call_gemini(
            market_overview_prompt(get_market_overview())
        ),
        "market_structure": call_gemini(
            bitcoin_structure_prompt(get_bitcoin_structure())
        ),
        "momentum_analysis": call_gemini(
            momentum_prompt(get_monthly_momentum())
        ),
        "risk_context": call_gemini(
            risk_prompt(get_ath_distribution())
        ),
        "generated_at": datetime.utcnow().isoformat()
    }
