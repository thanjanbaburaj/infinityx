# console/pages/4_Referrals.py

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records, create_record  # type: ignore


st.set_page_config(page_title="Referrals", page_icon="🔗", layout="wide")


def main():
    st.title("Referrals")

    referrals = read_records("REFERRALS")
    st.write(f"Total referrals: {len(referrals)}")

    with st.expander("Add New Referral"):
        with st.form("new_referral_form"):
            from_client = st.text_input("From Client ID")
            to_name = st.text_input("Referred Name")
            to_phone = st.text_input("Referred Phone")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Create Referral")
            if submitted and from_client and to_name:
                create_record(
                    "REFERRALS",
                    {
                        "FromClientID": from_client,
                        "Name": to_name,
                        "Phone": to_phone,
                        "Notes": notes,
                    },
                )
                st.success("Referral created. Please refresh to see the update.")

    st.markdown("---")
    st.subheader("Referral List")

    if not referrals:
        st.info("No referrals yet.")
        return

    st.table(
        [
            {
                "FromClientID": r.get("FromClientID", ""),
                "Name": r.get("Name", ""),
                "Phone": r.get("Phone", ""),
                "Notes": r.get("Notes", ""),
            }
            for r in referrals
        ]
    )


if __name__ == "__main__":
    main()
