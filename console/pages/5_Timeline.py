# console/pages/5_Timeline.py

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records  # type: ignore


st.set_page_config(page_title="Timeline", page_icon="📜", layout="wide")


def main():
    st.title("Client Timeline")

    client_id = st.text_input("Client ID", value=st.session_state.get("selected_client_id", "") or "")
    if not client_id:
        st.info("Enter a Client ID or select one from the main app sidebar.")
        return

    interactions = read_records("INTERACTIONS", filters={"ClientID": client_id})

    st.write(f"Total interactions for {client_id}: {len(interactions)}")

    if not interactions:
        st.info("No interactions logged yet.")
        return

    st.table(
        [
            {
                "Date": i.get("Date", ""),
                "Type": i.get("Type", ""),
                "Notes": i.get("Notes", ""),
            }
            for i in interactions
        ]
    )


if __name__ == "__main__":
    main()
