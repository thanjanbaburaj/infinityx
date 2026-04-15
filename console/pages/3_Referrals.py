# console/pages/3_Referrals.py
import streamlit as st
from shared.sheets import read_rows, create_row
from shared.utils import iso_to_date_str

st.set_page_config(page_title="Referrals", page_icon="🔗", layout="wide")

st.title("Referrals")

tab_list, tab_add = st.tabs(["Referral List", "Add Referral"])

with tab_list:
    st.subheader("Referral List")
    try:
        rows = read_rows("REFERRALS")
        if not rows:
            st.info("No referrals yet.")
        else:
            for r in rows:
                label = f"{r.get('ref_name','')} → {r.get('full_name','')} ({r.get('ref_status','')})"
                with st.expander(label):
                    st.write(f"**Referral ID:** {r.get('referral_id','')}")
                    st.write(f"**Client ID:** {r.get('client_id','')}")
                    st.write(f"**Client Name:** {r.get('full_name','')}")
                    st.write(f"**Ref Mobile:** {r.get('ref_mobile','')}")
                    st.write(f"**Ref Email:** {r.get('ref_email','')}")
                    st.write(f"**Status:** {r.get('ref_status','')}")
                    st.write(f"**Notes:** {r.get('notes','')}")
                    st.write(f"**Created:** {iso_to_date_str(r.get('created_at'))}")
                    st.write(f"**Updated:** {iso_to_date_str(r.get('updated_at'))}")
    except Exception as e:
        st.error(f"Error loading referrals: {e}")

with tab_add:
    st.subheader("Add New Referral")
    client_id = st.text_input("Client ID (who referred)")
    full_name = st.text_input("Client Name")
    ref_name = st.text_input("Referral Name")
    ref_mobile = st.text_input("Referral Mobile")
    ref_email = st.text_input("Referral Email")
    ref_status = st.selectbox("Referral Status", ["new", "contacted", "converted", "lost"])
    notes = st.text_area("Notes")

    if st.button("Create Referral", type="primary"):
        payload = {
            "client_id": client_id,
            "full_name": full_name,
            "ref_name": ref_name,
            "ref_mobile": ref_mobile,
            "ref_email": ref_email,
            "ref_status": ref_status,
            "notes": notes,
        }
        try:
            res = create_row("REFERRALS", payload)
            st.success("Referral created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error creating referral: {e}")
