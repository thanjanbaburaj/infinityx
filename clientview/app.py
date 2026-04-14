# clientview/app.py

import sys
from pathlib import Path

import streamlit as st

# Ensure shared/ is importable when running from clientview/
sys.path.append(str(Path(__file__).resolve().parent.parent))

from shared import read_records  # type: ignore


st.set_page_config(
    page_title="Infinity-X ClientView",
    page_icon="👁️",
    layout="wide",
)


def init_session():
    if "client_email" not in st.session_state:
        st.session_state.client_email = ""


def main():
    init_session()
    st.title("Infinity-X ClientView")

    st.write(
        "Welcome. This is your personal view of your profile, fact-find, "
        "summary, and recommendations."
    )

    email = st.text_input(
        "Enter your registered email",
        value=st.session_state.get("client_email", ""),
    )
    if email:
        st.session_state.client_email = email

        clients = read_records("CLIENTS", filters={"Email": email})
        if not clients:
            st.error("No client found with this email.")
        else:
            client = clients[0]
            st.success(f"Welcome, {client.get('Name', '')}. Use the pages on the left to navigate.")


if __name__ == "__main__":
    main()
