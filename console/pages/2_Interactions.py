# console/pages/2_Interactions.py
import streamlit as st
from shared.sheets import read_rows, create_row
from shared.utils import iso_to_date_str

st.set_page_config(page_title="Interactions", page_icon="📞", layout="wide")

st.title("Interactions")

tab_list, tab_add = st.tabs(["Timeline", "Log Interaction"])

with tab_list:
    st.subheader("Recent Interactions")
    try:
        rows = read_rows("INTERACTIONS")
        if not rows:
            st.info("No interactions logged yet.")
        else:
            rows_sorted = sorted(
                rows,
                key=lambda r: str(r.get("date") or ""),
                reverse=True,
            )
            for r in rows_sorted:
                label = f"{r.get('date','')} — {r.get('type','')} — {r.get('full_name','')}"
                with st.expander(label):
                    st.write(f"**Client ID:** {r.get('client_id','')}")
                    st.write(f"**Channel:** {r.get('channel','')}")
                    st.write(f"**Summary:** {r.get('summary','')}")
                    st.write(f"**Outcome:** {r.get('outcome','')}")
                    st.write(f"**Next Action:** {r.get('next_action','')}")
                    st.write(f"**Next Action Date:** {r.get('next_action_date','')}")
                    st.write(f"**Created:** {iso_to_date_str(r.get('created_at'))}")
                    st.write(f"**Updated:** {iso_to_date_str(r.get('updated_at'))}")
    except Exception as e:
        st.error(f"Error loading interactions: {e}")

with tab_add:
    st.subheader("Log New Interaction")
    client_id = st.text_input("Client ID")
    full_name = st.text_input("Client Name")
    date = st.date_input("Date")
    itype = st.selectbox("Type", ["call", "meeting", "whatsapp", "email", "other"])
    channel = st.text_input("Channel", "whatsapp")
    summary = st.text_area("Summary")
    outcome = st.text_area("Outcome")
    next_action = st.text_input("Next Action")
    next_action_date = st.date_input("Next Action Date", value=None)

    if st.button("Save Interaction", type="primary"):
        payload = {
            "client_id": client_id,
            "full_name": full_name,
            "date": str(date),
            "type": itype,
            "channel": channel,
            "summary": summary,
            "outcome": outcome,
            "next_action": next_action,
            "next_action_date": str(next_action_date) if next_action_date else "",
        }
        try:
            res = create_row("INTERACTIONS", payload)
            st.success("Interaction logged.")
            st.json(res)
        except Exception as e:
            st.error(f"Error logging interaction: {e}")
