# clientview/pages/1_Profile.py

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records  # type: ignore
from clientview.components.widgets import profile_card  # type: ignore


st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")


def main():
    st.title("Your Profile")

    email = st.session_state.get("client_email", "")
    if not email:
        st.info("Please enter your email on the main page first.")
        return

    clients = read_records("CLIENTS", filters={"Email": email})
    if not clients:
        st.error("No client found with this email.")
        return

    client = clients[0]
    profile_card(client)

    st.markdown("---")
    st.write("If any of these details are incorrect, please contact your advisor to update them.")


if __name__ == "__main__":
    main()
