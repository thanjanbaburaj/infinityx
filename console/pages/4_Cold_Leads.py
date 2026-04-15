# console/pages/4_Cold_Leads.py
import streamlit as st
from shared.sheets import read_rows, create_row
from shared.utils import iso_to_date_str

st.set_page_config(page_title="Cold Leads", page_icon="🥶", layout="wide")

st.title("Cold Leads")

tab_list, tab_add = st.tabs(["Lead List", "Add Lead"])

with tab_list:
    st.subheader("Lead List")
    try:
        rows = read_rows("Cold_Leads")
        if not rows:
            st.info("No cold leads yet.")
        else:
            rows_sorted = sorted(
                rows,
                key=lambda r: str(r.get("LeadScore") or ""),
                reverse=True,
            )
            for r in rows_sorted:
                label = f"{r.get('FullName','')} — Score: {r.get('LeadScore','')}"
                with st.expander(label):
                    st.write(f"**Lead ID:** {r.get('LeadID','')}")
                    st.write(f"**Mobile:** {r.get('Mobile','')}")
                    st.write(f"**Email:** {r.get('Email','')}")
                    st.write(f"**Source:** {r.get('Source','')}")
                    st.write(f"**Trigger Type:** {r.get('TriggerType','')}")
                    st.write(f"**Q1:** {r.get('Q1','')}")
                    st.write(f"**Q2:** {r.get('Q2','')}")
                    st.write(f"**Q3:** {r.get('Q3','')}")
                    st.write(f"**Salary Band:** {r.get('SalaryBand','')}")
                    st.write(f"**Lead Score:** {r.get('LeadScore','')}")
                    st.write(f"**Status:** {r.get('Status','')}")
                    st.write(f"**Last Contact:** {iso_to_date_str(r.get('LastContactAt'))}")
                    st.write(f"**Next Action Date:** {iso_to_date_str(r.get('NextActionDate'))}")
                    st.write(f"**Created:** {iso_to_date_str(r.get('CreatedAt'))}")
                    st.write(f"**Updated:** {iso_to_date_str(r.get('UpdatedAt'))}")
    except Exception as e:
        st.error(f"Error loading cold leads: {e}")

with tab_add:
    st.subheader("Add Cold Lead")
    full_name = st.text_input("Full Name")
    mobile = st.text_input("Mobile")
    email = st.text_input("Email")
    source = st.text_input("Source")
    trigger_type = st.text_input("Trigger Type")
    q1 = st.text_input("Q1")
    q2 = st.text_input("Q2")
    q3 = st.text_input("Q3")
    salary_band = st.text_input("Salary Band")
    lead_score = st.text_input("Lead Score")
    status = st.selectbox("Status", ["new", "contacted", "nurture", "closed"])

    if st.button("Create Lead", type="primary"):
        payload = {
            "FullName": full_name,
            "Mobile": mobile,
            "Email": email,
            "Source": source,
            "TriggerType": trigger_type,
            "Q1": q1,
            "Q2": q2,
            "Q3": q3,
            "SalaryBand": salary_band,
            "LeadScore": lead_score,
            "Status": status,
        }
        try:
            res = create_row("Cold_Leads", payload)
            st.success("Lead created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error creating lead: {e}")
