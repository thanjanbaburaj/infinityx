# console/pages/6_Review_Intelligence.py

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records  # type: ignore
from shared.utils import format_currency  # type: ignore


st.set_page_config(page_title="Review Intelligence", page_icon="🧠", layout="wide")


def main():
    st.title("Review Intelligence")

    client_id = st.text_input("Client ID", value=st.session_state.get("selected_client_id", "") or "")
    if not client_id:
        st.info("Enter a Client ID or select one from the main app sidebar.")
        return

    policies = read_records("POLICIES", filters={"ClientID": client_id})

    if not policies:
        st.info("No policies found for this client.")
        return

    st.subheader("Policy Snapshot")
    total_premium = sum(float(p.get("Premium", 0) or 0) for p in policies)
    st.metric("Total Annual Premium", format_currency(total_premium))

    st.markdown("---")
    st.subheader("Quick Review Notes")
    st.write(
        "- Check if life cover is adequate vs income.\n"
        "- Check if medical cover is aligned with family size.\n"
        "- Check if savings/investment policies match goals and time horizon.\n"
        "- Identify upgrade, consolidation, or protection gaps."
    )


if __name__ == "__main__":
    main()
