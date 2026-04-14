# console/pages/2_Leads.py

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records, create_record  # type: ignore


st.set_page_config(page_title="Leads", page_icon="📇", layout="wide")


def main():
    st.title("Leads")

    leads = read_records("LEADS")
    st.write(f"Total leads: {len(leads)}")

    with st.expander("Add New Lead"):
        with st.form("new_lead_form"):
            name = st.text_input("Name")
            phone = st.text_input("Phone")
            source = st.text_input("Source")
            submitted = st.form_submit_button("Create Lead")
            if submitted and name:
                create_record(
                    "LEADS",
                    {"Name": name, "Phone": phone, "Source": source},
                )
                st.success("Lead created. Please refresh to see the update.")

    st.markdown("---")
    st.subheader("Lead List")

    if not leads:
        st.info("No leads yet.")
        return

    st.table(
        [
            {
                "Name": l.get("Name", ""),
                "Phone": l.get("Phone", ""),
                "Source": l.get("Source", ""),
                "Status": l.get("Status", ""),
            }
            for l in leads
        ]
    )


if __name__ == "__main__":
    main()
