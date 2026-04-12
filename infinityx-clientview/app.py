import streamlit as st
from shared import config
from shared.api import apps_script_client as api
from shared.models import review_models as rm
from shared.utils import formatting as fmt

st.set_page_config(page_title="Infinity-X ClientView", layout="wide")

# --- Auth ---
password = st.text_input("Enter access password", type="password")
if password != config.get_clientview_password():
    st.stop()

st.title("Your Financial Review")

client_id = st.text_input("Your Client ID")

if st.button("View Review Summary"):
    if not client_id:
        st.warning("Enter your Client ID")
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

            st.subheader("Architecture")
            arch = summary["architecture"]
            st.write({
                "MUST": arch["must"],
                "SHOULD": arch["should"],
                "COULD": arch["could"],
            })

            st.subheader("Blueprint Notes")
            bp = summary["blueprint"]
            st.write(bp["advisor_notes"])
