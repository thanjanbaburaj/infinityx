# clientview/pages/3_Summary.py

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records  # type: ignore
from shared.utils import format_currency  # type: ignore


st.set_page_config(page_title="Summary", page_icon="📊", layout="wide")


def main():
    st.title("Your Protection & Savings Summary")

    email = st.session_state.get("client_email", "")
    if not email:
        st.info("Please enter your email on the main page first.")
        return

    clients = read_records("CLIENTS", filters={"Email": email})
    if not clients:
        st.error("No client found with this email.")
        return

    client = clients[0]
    client_id = client.get("ClientID", "")

    if not client_id:
        st.error("ClientID missing for this profile.")
        return

    policies = read_records("POLICIES", filters={"ClientID": client_id})

    if not policies:
        st.info("No policies found yet.")
        return

    total_premium = sum(float(p.get("Premium", 0) or 0) for p in policies)

    st.subheader("At a Glance")
    col1, col2 = st.columns(2)
    col1.metric("Number of Policies", len(policies))
    col2.metric("Total Annual Premium", format_currency(total_premium))

    st.markdown("---")
    st.subheader("Policy List")

    st.table(
        [
            {
                "Policy #": p.get("PolicyNumber", ""),
                "Product": p.get("Product", ""),
                "Premium": format_currency(p.get("Premium", 0)),
                "Status": p.get("Status", ""),
            }
            for p in policies
        ]
    )


if __name__ == "__main__":
    main()
