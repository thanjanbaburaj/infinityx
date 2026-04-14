# console/app.py

import sys
from pathlib import Path

import streamlit as st

# Ensure shared/ is importable when running from console/
sys.path.append(str(Path(__file__).resolve().parent.parent))

from shared import read_records  # type: ignore


st.set_page_config(
    page_title="Infinity-X Console",
    page_icon="🧭",
    layout="wide",
)


def init_session():
    if "selected_client_id" not in st.session_state:
        st.session_state.selected_client_id = None


def sidebar_client_selector():
    st.sidebar.title("Infinity-X Console")
    st.sidebar.caption("Advisor View")

    clients = read_records("CLIENTS")
    options = ["-- Select Client --"] + [
        f"{c.get('ClientID', '')} - {c.get('Name', '')}" for c in clients
    ]
    choice = st.sidebar.selectbox("Active Client", options)

    if choice != "-- Select Client --":
        client_id = choice.split(" - ")[0]
        st.session_state.selected_client_id = client_id
    else:
        st.session_state.selected_client_id = None

    st.sidebar.markdown("---")
    st.sidebar.write("Use the pages on the left to navigate.")


def main():
    init_session()
    sidebar_client_selector()
    st.title("Infinity-X Advisor Console")
    st.write(
        "Use the sidebar to select a client and navigate between Clients, Leads, "
        "Meetings, Referrals, Timeline, Review Intelligence, and Backend Health."
    )


if __name__ == "__main__":
    main()
