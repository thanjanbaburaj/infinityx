# console/components/widgets.py

from typing import Dict, Any, List

import streamlit as st

from shared.utils import format_currency, parse_date, safe_get


def client_summary_card(client: Dict[str, Any]):
    st.markdown("### Client Summary")
    cols = st.columns(3)
    cols[0].metric("Name", safe_get(client, "Name"))
    cols[1].metric("Phone", safe_get(client, "Phone"))
    cols[2].metric("Email", safe_get(client, "Email"))


def policy_table(policies: List[Dict[str, Any]]):
    if not policies:
        st.info("No policies found for this client.")
        return

    rows = []
    for p in policies:
        rows.append(
            {
                "Policy #": safe_get(p, "PolicyNumber"),
                "Product": safe_get(p, "Product"),
                "Premium": format_currency(safe_get(p, "Premium")),
                "Status": safe_get(p, "Status"),
                "Start": parse_date(safe_get(p, "StartDate")),
            }
        )
    st.table(rows)
