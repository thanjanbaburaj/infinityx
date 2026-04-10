import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time

st.set_page_config(page_title="Backend Health Dashboard", page_icon="📊", layout="wide")

st.title("📊 Infinity‑X Backend Health Dashboard")
st.caption("Quick view of JSON key, Google auth, sheet access, and tab health.")

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

DEFAULT_SHEET_NAME = "Infinity-X Backend"
EXPECTED_TABS = [
    "Cold Leads",
    "Clients",
    "Policies",
    "Interactions",
    "Financial_Fact_Find",
    "Config",
]

# ---------- 1. JSON Key Status ----------
st.subheader("1️⃣ JSON Key Status")

raw_json = st.secrets.get("GOOGLE_SERVICE_ACCOUNT_JSON", None)

if not raw_json:
    st.error("❌ No GOOGLE_SERVICE_ACCOUNT_JSON found in Streamlit Secrets.")
    st.stop()

json_ok = False
parsed = None

try:
    parsed = json.loads(raw_json)
    json_ok = True
    st.success("✅ JSON is valid and correctly formatted.")
except Exception as e:
    st.error("❌ JSON is NOT valid. Fix your Streamlit secret.")
    st.code(str(e))
    st.stop()

# ---------- 2. Authentication Status ----------
st.subheader("2️⃣ Google Authentication Status")

auth_ok = False
gc = None

if json_ok:
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_dict(parsed, SCOPE)
        gc = gspread.authorize(creds)
        auth_ok = True
        st.success("✅ Authentication successful. Google accepted your credentials.")
        st.write(f"Service account: `{parsed.get('client_email', 'N/A')}`")
    except Exception as e:
        st.error("❌ Authentication failed. Check private key / formatting.")
        st.code(str(e))
        st.stop()

# ---------- 3. Sheet Access & Tabs ----------
st.subheader("3️⃣ Sheet Access & Tabs")

sheet_name = st.text_input("Backend Sheet Name", value=DEFAULT_SHEET_NAME)

sheet_ok = False
tabs = []

if auth_ok and st.button("Run Sheet Health Check"):
    with st.spinner("Checking sheet access..."):
        try:
            sh = gc.open(sheet_name)
            sheet_ok = True
            st.success(f"✅ Successfully accessed Google Sheet: `{sheet_name}`")

            tabs = [ws.title for ws in sh.worksheets()]
            st.write("**Available Tabs:**", tabs)

            missing_tabs = [t for t in EXPECTED_TABS if t not in tabs]
            extra_tabs = [t for t in tabs if t not in EXPECTED_TABS]

            if missing_tabs:
                st.warning(f"⚠️ Missing expected tabs: {missing_tabs}")
            else:
                st.success("✅ All expected tabs exist.")

            if extra_tabs:
                st.info(f"ℹ️ Extra tabs present (not required but okay): {extra_tabs}")

        except Exception as e:
            st.error("❌ Could not access the sheet. Check name or sharing permissions.")
            st.code(str(e))

# ---------- 4. Tab Row Counts ----------
st.subheader("4️⃣ Tab Row Counts & Read Latency")

if sheet_ok:
    col_main, col_side = st.columns([3, 1])
    with col_side:
        run_counts = st.button("Refresh Row Counts")

    if run_counts:
        results = []
        for tab in EXPECTED_TABS:
            try:
                ws = sh.worksheet(tab)
                start = time.time()
                data = ws.get_all_values()
                elapsed = time.time() - start
                row_count = max(len(data) - 1, 0)  # minus header
                results.append({
                    "Tab": tab,
                    "Rows": row_count,
                    "Read Time (s)": round(elapsed, 3),
                    "Status": "OK" if row_count >= 0 else "Check",
                })
            except Exception as e:
                results.append({
                    "Tab": tab,
                    "Rows": "ERR",
                    "Read Time (s)": "-",
                    "Status": f"Error: {str(e)[:40]}",
                })

        df = pd.DataFrame(results)
        col_main.dataframe(df, use_container_width=True)

        st.caption("Row counts help you see if data is flowing. Read time shows if anything is unusually slow.")

# ---------- 5. Quick Interpretation ----------
st.subheader("5️⃣ Quick Interpretation Guide")

st.markdown("""
- ✅ **JSON valid + Auth OK + Sheet OK** → Backend is healthy.
- ⚠️ **Missing tabs** → Fix sheet structure before using Infinity‑X fully.
- ❌ **Auth or sheet errors** → Check JSON formatting, service account sharing, or sheet name.
""")
