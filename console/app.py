# console/app.py
import streamlit as st

st.set_page_config(
    page_title="Infinity-X Console",
    page_icon="🧭",
    layout="wide",
)

st.title("Infinity-X Advisor Console")
st.write("Your cockpit for daily execution, follow-ups, and client intelligence.")

st.markdown("### Navigation")
st.write("Use the left sidebar to switch between pages (Clients, Interactions, Referrals, Cold Leads, Policy Funds, Backend Health).")
