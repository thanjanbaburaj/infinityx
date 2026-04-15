# console/pages/1_Clients.py
import streamlit as st
from shared.sheets import read_rows, create_row
from shared.utils import iso_to_date_str

st.set_page_config(page_title="Clients", page_icon="👥", layout="wide")

st.title("Clients")

tab_list, tab_add = st.tabs(["Client List", "Add Client"])

with tab_list:
    st.subheader("Client List")
    try:
        rows = read_rows("CLIENTS")
        if not rows:
            st.info("No clients yet.")
        else:
            for r in rows:
                name = r.get("full_name") or f"{r.get('first_name','')} {r.get('last_name','')}".strip()
                label = f"{name} — {r.get('status','')}"
                with st.expander(label):
                    st.write(f"**Client ID:** {r.get('client_id','')}")
                    st.write(f"**Mobile:** {r.get('mobile','')}")
                    st.write(f"**Email:** {r.get('email','')}")
                    st.write(f"**Segment:** {r.get('segment','')}")
                    st.write(f"**Lead Source:** {r.get('lead_source','')}")
                    st.write(f"**Lead Score:** {r.get('lead_score','')}")
                    st.write(f"**Created:** {iso_to_date_str(r.get('created_at'))}")
                    st.write(f"**Updated:** {iso_to_date_str(r.get('updated_at'))}")
                    st.write(f"**Notes:** {r.get('notes','')}")
    except Exception as e:
        st.error(f"Error loading clients: {e}")

with tab_add:
    st.subheader("Add New Client")
    full_name = st.text_input("Full Name")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    mobile = st.text_input("Mobile")
    email = st.text_input("Email")
    status = st.selectbox("Status", ["prospect", "active", "inactive", "lost"])
    segment = st.selectbox("Segment", ["A", "B", "C", "Unassigned"])
    lead_source = st.text_input("Lead Source", "manual")
    lead_score = st.selectbox("Lead Score", ["cold", "warm", "hot"])
    notes = st.text_area("Notes")

    if st.button("Create Client", type="primary"):
        if not (full_name or first_name):
            st.warning("At least Full Name or First Name is required.")
        else:
            payload = {
                "full_name": full_name or f"{first_name} {last_name}".strip(),
                "first_name": first_name,
                "last_name": last_name,
                "mobile": mobile,
                "email": email,
                "status": status,
                "segment": segment,
                "lead_source": lead_source,
                "lead_score": lead_score,
                "notes": notes,
            }
            try:
                res = create_row("CLIENTS", payload)
                st.success("Client created.")
                st.json(res)
            except Exception as e:
                st.error(f"Error creating client: {e}")
