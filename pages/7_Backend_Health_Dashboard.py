import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

st.set_page_config(page_title="Backend Health Dashboard", page_icon="📊", layout="wide")
st.title("📊 Infinity‑X Backend Health Dashboard")
st.caption("Quick view of service account, Google auth, sheet access, and tab health.")

# ---------------------------------------------------------
# 1️⃣ CHECK SERVICE ACCOUNT BLOCK
# ---------------------------------------------------------
st.subheader("1️⃣ Service Account Status")

service_block = st.secrets.get("gcp_service_account", None)

if not service_block:
    st.error("❌ No [gcp_service_account] block found in secrets.toml.")
    st.stop()

st.success("✅ Service account block found in secrets.toml")
st.write(f"**Client Email:** `{service_block.get('client_email', 'N/A')}`")
st.write(f"**Project ID:** `{service_block.get('project_id', 'N/A')}`")

# ---------------------------------------------------------
# 2️⃣ CHECK GOOGLE AUTHENTICATION
# ---------------------------------------------------------
st.subheader("2️⃣ Google Authentication")

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_block, SCOPE)
    gc = gspread.authorize(creds)
    st.success("✅ Google authentication successful")
except Exception as e:
    st.error("❌ Google authentication failed")
    st.code(str(e))
    st.stop()

# ---------------------------------------------------------
# 3️⃣ CHECK SPREADSHEET ACCESS
# ---------------------------------------------------------
st.subheader("3️⃣ Spreadsheet Access")

spreadsheet_id = st.secrets.get("spreadsheet_id", None)

if not spreadsheet_id:
    st.error("❌ No spreadsheet_id found in secrets.toml.")
    st.stop()

try:
    sh = gc.open_by_key(spreadsheet_id)
    st.success(f"✅ Spreadsheet loaded successfully")
    st.write(f"**Spreadsheet Title:** `{sh.title}`")
except Exception as e:
    st.error("❌ Failed to open spreadsheet using spreadsheet_id")
    st.code(str(e))
    st.stop()

# ---------------------------------------------------------
# 4️⃣ CHECK TAB HEALTH
# ---------------------------------------------------------
st.subheader("4️⃣ Worksheet (Tab) Health")

required_tabs = [
    "Cold_Leads",
    "Clients",
    "Policies",
    "Interactions",
    "Financial_Fact_Find",
]

tab_status = {}

for tab in required_tabs:
    try:
        ws = sh.worksheet(tab)
        rows = len(ws.get_all_values())
        tab_status[tab] = f"✅ Exists — {rows} rows"
    except Exception:
        tab_status[tab] = "❌ Missing"

for tab, status in tab_status.items():
    if "❌" in status:
        st.error(f"{tab}: {status}")
    else:
        st.success(f"{tab}: {status}")

# ---------------------------------------------------------
# 5️⃣ LATENCY TEST
# ---------------------------------------------------------
st.subheader("5️⃣ Read Latency Test")

try:
    start = time.time()
    _ = sh.sheet1.get_all_values()
    latency = round((time.time() - start) * 1000, 2)
    st.success(f"✅ Read latency: {latency} ms")
except Exception as e:
    st.error("❌ Latency test failed")
    st.code(str(e))
