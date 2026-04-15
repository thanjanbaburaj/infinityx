# console/app.py
import streamlit as st

st.set_page_config(
    page_title="Infinity-X Console",
    page_icon="🧭",
    layout="wide",
)

st.title("Infinity-X Advisor Console")
st.write("Your cockpit for daily execution, follow-ups, and client intelligence.")

st.markdown("### How to use this console (v1.0)")
st.markdown(
    """
- **Clients:** manage your pipeline (prospects + clients).
- **Interactions:** log calls, meetings, WhatsApp, follow-ups.
- **Referrals:** track introductions and their status.
- **Cold Leads:** store and score cold leads.
- **Policy Funds:** view fund allocations and values.
- **Backend Health:** quick check that Sheets + Apps Script are OK.

Use the left sidebar to switch between pages.
"""
)
