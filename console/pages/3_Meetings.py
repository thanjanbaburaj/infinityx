# console/pages/3_Meetings.py

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records, create_record  # type: ignore


st.set_page_config(page_title="Meetings", page_icon="📅", layout="wide")


def main():
    st.title("Meetings")

    meetings = read_records("MEETINGS")
    st.write(f"Total meetings: {len(meetings)}")

    with st.expander("Log New Meeting"):
        with st.form("new_meeting_form"):
            client_id = st.text_input("Client ID")
            date = st.date_input("Date")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Log Meeting")
            if submitted and client_id:
                create_record(
                    "MEETINGS",
                    {
                        "ClientID": client_id,
                        "Date": str(date),
                        "Notes": notes,
                    },
                )
                st.success("Meeting logged. Please refresh to see the update.")

    st.markdown("---")
    st.subheader("Meeting Log")

    if not meetings:
        st.info("No meetings logged yet.")
        return

    st.table(
        [
            {
                "ClientID": m.get("ClientID", ""),
                "Date": m.get("Date", ""),
                "Notes": m.get("Notes", ""),
            }
            for m in meetings
        ]
    )


if __name__ == "__main__":
    main()
