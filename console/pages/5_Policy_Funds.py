# console/pages/5_Policy_Funds.py
import streamlit as st
from shared.sheets import read_rows
from shared.utils import iso_to_date_str

st.set_page_config(page_title="Policy Funds", page_icon="📊", layout="wide")

st.title("Policy Funds")

st.subheader("All Funds")

try:
    rows = read_rows("Policy_Funds")
    if not rows:
        st.info("No policy funds yet.")
    else:
        df_rows = []
        for r in rows:
            df_rows.append({
                "FundID": r.get("FundID",""),
                "PolicyID": r.get("PolicyID",""),
                "ClientID": r.get("ClientID",""),
                "FullName": r.get("FullName",""),
                "Carrier": r.get("Carrier",""),
                "FundName": r.get("FundName",""),
                "ISIN": r.get("ISIN",""),
                "AllocationPercent": r.get("AllocationPercent",""),
                "UnitsHeld": r.get("UnitsHeld",""),
                "UnitPrice_Carrier": r.get("UnitPrice_Carrier",""),
                "UnitPrice_YF": r.get("UnitPrice_YF",""),
                "CurrentValue": r.get("CurrentValue",""),
                "LastUpdated": iso_to_date_str(r.get("LastUpdated")),
            })
        st.dataframe(df_rows, use_container_width=True)
except Exception as e:
    st.error(f"Error loading policy funds: {e}")
