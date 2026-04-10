import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="JSON Key Checker", page_icon="🛠️", layout="wide")

st.title("🔐 Infinity‑X JSON Key Checker")
st.markdown("Use this tool to validate your Google Service Account JSON and test your backend connection.")

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# ---------------------------
# 1. Validate JSON Format
# ---------------------------
st.subheader("1️⃣ JSON Format Validation")

raw_json = st.secrets.get("GOOGLE_SERVICE_ACCOUNT_JSON", None)

if not raw_json:
    st.error("❌ No GOOGLE_SERVICE_ACCOUNT_JSON found in Streamlit Secrets.")
    st.stop()

try:
    parsed = json.loads(raw_json)
    st.success("✅ JSON is valid and correctly formatted.")
except Exception as e:
    st.error("❌ JSON is NOT valid. Fix your Streamlit secret.")
    st.code(str(e))
    st.stop()

# ---------------------------
# 2. Validate Required Fields
# ---------------------------
st.subheader("2️⃣ Required Fields Check")

required_fields = [
    "type", "project_id", "private_key_id", "private_key",
    "client_email", "client_id"
]

missing = [f for f in required_fields if f not in parsed]

if missing:
    st.error(f"❌ Missing required fields: {missing}")
else:
    st.success("✅ All required fields are present.")

# ---------------------------
# 3. Test Google Authentication
# ---------------------------
st.subheader("3️⃣ Authentication Test")

try:
    creds = ServiceAccountCredentials.from_json_keyfile_dict(parsed, SCOPE)
    gc = gspread.authorize(creds)
    st.success("✅ Authentication successful. Google accepted your credentials.")
except Exception as e:
    st.error("❌ Authentication failed. Your private key or formatting is incorrect.")
    st.code(str(e))
    st.stop()

# ---------------------------
# 4. Test Sheet Access
# ---------------------------
st.subheader("4️⃣ Google Sheet Access Test")

sheet_name = st.text_input("Enter your backend sheet name", "Infinity-X Backend")

if st.button("Test Sheet Access"):
    try:
        sh = gc.open(sheet_name)
        st.success(f"✅ Successfully accessed Google Sheet: {sheet_name}")

        tabs = [ws.title for ws in sh.worksheets()]
        st.write("### Available Tabs:")
        st.write(tabs)

        expected_tabs = [
            "Cold Leads", "Clients", "Policies", "Interactions",
            "Financial_Fact_Find", "Config"
        ]

        missing_tabs = [t for t in expected_tabs if t not in tabs]

        if missing_tabs:
            st.warning(f"⚠️ Missing expected tabs: {missing_tabs}")
        else:
            st.success("✅ All expected tabs exist.")

    except Exception as e:
        st.error("❌ Could not access the sheet. Check sharing permissions.")
        st.code(str(e))
