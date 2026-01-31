from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import sys
import os
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from ai_insights_layer_02.gemini_insights import generate_full_market_insight


# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------

st.set_page_config(
    page_title="CryptoLens AI — Market Insights",
    layout="wide"
)

st.title("CryptoLens AI — Market Insights")


# ---------------------------------------------------------
# Power BI Embed
# ---------------------------------------------------------

st.subheader("Interactive Market Dashboard")

POWER_BI_EMBED_URL = """
https://app.powerbi.com/view?r=eyJrIjoiZDg3MGUyMjQtZjJlZC00MmZmLTk2NTItZTQyOGI5Y2ZjMTcxIiwidCI6IjA0MzJkMmY1LTA0MzUtNGJjMy1iNDBjLThhOTdmZTJkODc2YSJ9
"""

st.components.v1.iframe(
    POWER_BI_EMBED_URL,
    height=600,
    scrolling=True
)

st.markdown("""
**AI-assisted interpretation of Power BI dashboards**

- Observational insights only  
- No predictions  
- No trading advice  
""")

st.divider()


# ---------------------------------------------------------
# Rate Limiting (SESSION-LEVEL)
# ---------------------------------------------------------

if "last_call_ts" not in st.session_state:
    st.session_state.last_call_ts = 0


# ---------------------------------------------------------
# Gemini Trigger
# ---------------------------------------------------------

st.subheader("AI-Generated Market Commentary")

generate_btn = st.button("Generate AI Market Insights")

import time  # <-- make sure this exists

if "last_call_ts" not in st.session_state:
    st.session_state.last_call_ts = 0


if generate_btn:
    now = time.time()

    if now - st.session_state.last_call_ts < 30:
        st.warning("Please wait 30 seconds before generating insights again.")
    else:
        st.session_state.last_call_ts = now

        with st.spinner("Analyzing dashboard metrics..."):
            insights = generate_full_market_insight()

        st.success("Insights generated")

        # ---- FULL WIDTH LAYOUT ----
        st.markdown("### Market Overview")
        st.write(insights["market_overview"])

        st.markdown("### Market Structure (Bitcoin View)")
        st.write(insights["market_structure"])

        st.markdown("### Momentum Analysis")
        st.write(insights["momentum_analysis"])

        st.markdown("### Risk Context (ATH Proximity)")
        st.write(insights["risk_context"])

        st.caption(f"Generated at: {insights['generated_at']}")

else:
    st.info("Click **Generate AI Market Insights** to generate commentary.")
