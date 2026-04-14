# clientview/pages/2_FactFind.py

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records  # type: ignore


st.set_page_config(page_title="Fact-Find", page_icon="📋", layout="wide")


def main():
    st.title("Your Fact-Find")

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

    fact_rows = read_records("FACTFIND", filters={"ClientID": client_id})

    if not fact_rows:
        st.info("Your fact-find has not been completed yet.")
        return

    fact = fact_rows[0]

    st.subheader("Personal & Financial Snapshot")
    for key, value in fact.items():
        st.write(f"**{key}:** {value}")


if __name__ == "__main__":
    main()
