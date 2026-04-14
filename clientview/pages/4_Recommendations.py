# clientview/pages/4_Recommendations.py

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records  # type: ignore


st.set_page_config(page_title="Recommendations", page_icon="💡", layout="wide")


def main():
    st.title("Your Advisor's Recommendations")

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

    recs = read_records("RECOMMENDATIONS", filters={"ClientID": client_id})

    if not recs:
        st.info("No recommendations have been published yet. Please check back after your review meeting.")
        return

    for r in recs:
        st.markdown("### Recommendation")
        st.write(r.get("Text", ""))
        st.markdown("---")


if __name__ == "__main__":
    main()
