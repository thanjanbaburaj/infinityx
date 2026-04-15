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
        for r in rows:
            with st.expander(f"{r.get('FundName','')} — {r.get('FullName','')}"):
                st.write(f"**Fund ID:** {r.get('FundID','')}")
                st.write(f"**Policy ID:** {r.get('PolicyID','')}")
                st.write(f"**Client ID:** {r.get('ClientID','')}")
                st.write(f"**Client Name:** {r.get('FullName','')}")
                st.write(f"**Carrier:** {r.get('Carrier','')}")
                st.write(f"**Fund Name:** {r.get('FundName','')}")
                st.write(f"**ISIN:** {r.get('ISIN','')}")
                st.write(f"**Allocation %:** {r.get('AllocationPercent','')}")
                st.write(f"**Units Held:** {r.get('UnitsHeld','')}")
                st.write(f"**Unit Price (Carrier):** {r.get('UnitPrice_Carrier','')}")
                st.write(f"**Unit Price (YF):** {r.get('UnitPrice_YF','')}")
                st.write(f"**Current Value:** {r.get('CurrentValue','')}")
                st.write(f"**Last Updated:** {iso_to_date_str(r.get('LastUpdated'))}")
except Exception as e:
    st.error(f"Error loading policy funds: {e}")
