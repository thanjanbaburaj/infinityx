# console/pages/1_Clients.py

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records, create_record  # type: ignore
from console.components.widgets import client_summary_card  # type: ignore


st.set_page_config(page_title="Clients", page_icon="👤", layout="wide")


def load_clients():
    return read_records("CLIENTS")


def main():
    st.title("Clients")

    clients = load_clients()
    st.write(f"Total clients: {len(clients)}")

    with st.expander("Add New Client"):
        with st.form("new_client_form"):
            name = st.text_input("Name")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
            submitted = st.form_submit_button("Create Client")
            if submitted and name:
                create_record(
                    "CLIENTS",
                    {"Name": name, "Phone": phone, "Email": email},
                )
                st.success("Client created. Please refresh to see the update.")

    st.markdown("---")
    st.subheader("Client List")

    for c in clients:
        with st.container():
            client_summary_card(c)
            st.markdown("---")


if __name__ == "__main__":
    main()

