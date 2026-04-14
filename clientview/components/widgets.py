# clientview/components/widgets.py

from typing import Dict, Any

import streamlit as st

from shared.utils import format_currency, parse_date, safe_get


def profile_card(client: Dict[str, Any]):
    st.markdown("### Your Profile")
    cols = st.columns(3)
    cols[0].metric("Name", safe_get(client, "Name"))
    cols[1].metric("Phone", safe_get(client, "Phone"))
    cols[2].metric("Email", safe_get(client, "Email"))


def policy_snapshot(policy: Dict[str, Any]):
    st.markdown("#### Policy")
    cols = st.columns(3)
    cols[0].write(f"**Product:** {safe_get(policy, 'Product')}")
    cols[1].write(f"**Premium:** {format_currency(safe_get(policy, 'Premium'))}")
    cols[2].write(f"**Status:** {safe_get(policy, 'Status')}")
    st.write(f"Start Date: {parse_date(safe_get(policy, 'StartDate'))}")
