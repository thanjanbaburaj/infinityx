# console/pages/7_Backend_Health.py
import streamlit as st
from shared.sheets import read_rows

st.set_page_config(page_title="Backend Health", page_icon="🩺", layout="wide")

st.title("Backend Health Dashboard")
st.write("Quick checks to ensure Sheets + Apps Script are responding correctly.")

sheets_to_check = [
    "CLIENTS",
    "FACTFIND",
    "POLICIES",
    "INTERACTIONS",
    "REFERRALS",
    "INBOUND_EVENTS",
    "ERROR_LOG",
    "CONFIG",
    "Policy_Funds",
    "Cold_Leads",
]

for name in sheets_to_check:
    try:
        rows = read_rows(name)
        st.success(f"{name}: OK ({len(rows)} rows)")
    except Exception as e:
        st.error(f"{name}: ERROR — {e}")
