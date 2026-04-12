import streamlit as st
from shared import config
from shared.api import apps_script_client as api
from shared.models import review_models as rm
from shared.utils import formatting as fmt

st.set_page_config(page_title="Infinity-X Console", layout="wide")

# --- Auth ---
password = st.text_input("Enter console password", type="password")
if password != config.get_console_password():
    st.stop()

st.title("Infinity-X Advisor Console")

client_id = st.text_input("Client ID", value="C0001")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Run Review Summary"):
        if not client_id:
            st.warning("Enter Client ID")
        else:
            summary = api.get_review_summary(client_id)
            if not rm.is_exists(summary):
                st.error(rm.get_message(summary))
            else:
                st.subheader("Snapshot")
                snap = summary["snapshot"]
                st.write({
                    "Income": fmt.money(snap["income"]),
                    "Expenses": fmt.money(snap["expenses"]),
                    "Surplus": fmt.money(snap["surplus"]),
                })
                st.subheader("Raw JSON")
                st.json(summary)

with col2:
    if st.button("WhatsApp Summary"):
        if not client_id:
            st.warning("Enter Client ID")
        else:
            wa = api.get_whatsapp_summary(client_id)
            if not wa.get("exists"):
                st.error(wa.get("message", "No summary"))
            else:
                st.subheader("WhatsApp Message")
                st.code(wa["message"])

with col3:
    if st.button("Follow-Up"):
        if not client_id:
            st.warning("Enter Client ID")
        else:
            fu = api.get_follow_up(client_id)
            if not fu.get("exists"):
                st.error(fu.get("message", "No follow-up"))
            else:
                st.subheader("Follow-Up Plan")
                st.write({
                    "Next Follow-Up Date": fu["next_followup_date"],
                })
                st.subheader("Recommended Message")
                st.code(fu["recommended_message"])
