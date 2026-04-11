import streamlit as st
import time
import pandas as pd
from utils.sheets import get_spreadsheet, load_sheet

st.set_page_config(page_title="Infinity-X Backend Health", page_icon="📊", layout="wide")

st.title("📊 Infinity‑X System Health Dashboard")
st.caption("Service account, Google auth, sheet access, tab health, schema health, and enhancements.")

# -----------------------------
# 1️⃣ Service Account & Auth
# -----------------------------
st.header("1️⃣ Service Account & Google Auth")

ok_sa = False
ok_ss = False

with st.spinner("Checking service account and auth..."):
    try:
        ss = get_spreadsheet()
        ok_sa = True
        ok_ss = True
        st.success("✅ Service account & Google auth OK")
        st.write(f"Spreadsheet Title: **{ss.title}**")
    except Exception as e:
        st.error(f"❌ Failed to authenticate or open spreadsheet.\n\n{e}")

if not (ok_sa and ok_ss):
    st.stop()

# -----------------------------
# 2️⃣ Tab Health
# -----------------------------
st.header("2️⃣ Worksheet (Tab) Health")

expected_tabs = [
    "Cold_Leads",
    "Clients",
    "Policies",
    "Policy_Funds",
    "Interactions",
    "Financial_Fact_Find",
    "Config",
]

tab_status = []

for tab in expected_tabs:
    try:
        ws = ss.worksheet(tab)
        rows = ws.row_values(1)
        tab_status.append((tab, True, len(rows)))
    except Exception:
        tab_status.append((tab, False, 0))

col1, col2 = st.columns(2)
with col1:
    for tab, exists, header_len in tab_status:
        if exists:
            st.markdown(f"✅ **{tab}** — Exists — {header_len} header columns")
        else:
            st.markdown(f"❌ **{tab}** — Missing")

# -----------------------------
# 3️⃣ Column Schema Health
# -----------------------------
st.header("3️⃣ Column Schema Health")

expected_schema = {
    "Cold_Leads": [
        "LeadID", "FullName", "Mobile", "Email", "Source", "TriggerType",
        "Q1", "Q2", "Q3", "SalaryBand", "LeadScore", "Status",
        "LastContactAt", "NextActionDate", "CreatedAt", "UpdatedAt",
    ],
    "Clients": [
        "ClientID", "FullName", "Mobile", "Email", "Salary",
        "Status", "ClientScore", "NextReviewDate", "ReferralAsked",
    ],
    "Policies": [
        "PolicyID", "ClientID", "FullName", "Product", "Premium", "Frequency",
        "Status", "IssueDate", "PaidToDate", "NextPremiumDue",
        "CommissionRate", "ExpectedAnnualCommission",
        "LifeCover", "CICover", "DisabilityCover", "CurrentValue",
        "PolicyType", "Carrier", "PolicyNumber",
    ],
    "Policy_Funds": [
        "FundID", "PolicyID", "ClientID", "FullName", "Carrier",
        "FundName", "ISIN", "AllocationPercent", "UnitsHeld",
        "UnitPrice_Carrier", "UnitPrice_YF", "CurrentValue", "LastUpdated",
    ],
    "Interactions": [
        "InteractionID", "LeadID/ClientID", "FullName", "DateTime",
        "Channel", "Outcome", "Notes", "NextActionDate",
    ],
    "Financial_Fact_Find": [
        "ClientID", "FullName", "Income", "Expenses", "Assets",
        "Liabilities", "Dependents", "Catalyst",
        "CoverLife", "CoverCI", "CoverDisability",
        "RetirementAge", "EducationGoal", "LastUpdated",
    ],
    "Config": [
        "LeadSources", "TriggerTypes", "StatusOptions",
        "PaymentFrequencies", "OutcomeTags",
    ],
}

for tab, expected_cols in expected_schema.items():
    st.markdown(f"#### 🧾 {tab}")
    try:
        records = load_sheet(tab)
        df = pd.DataFrame(records)
        actual_cols = list(df.columns)
    except Exception as e:
        st.error(f"❌ Could not load '{tab}': {e}")
        continue

    missing = [c for c in expected_cols if c not in actual_cols]
    extra = [c for c in actual_cols if c not in expected_cols]

    if not missing and not extra:
        st.success("✅ Columns match expected schema.")
    else:
        if missing:
            st.error(f"❌ Missing columns: {missing}")
        if extra:
            st.markdown(f"🟡 Extra / enhancement columns: {extra}")

# -----------------------------
# 4️⃣ Read Latency
# -----------------------------
st.header("4️⃣ Read Latency Test")

start = time.time()
_ = load_sheet("Clients")
latency = (time.time() - start) * 1000
st.success(f"✅ Read latency: {latency:.2f} ms")

# -----------------------------
# 5️⃣ Enhancements Summary
# -----------------------------
st.header("5️⃣ Enhancements & Stability")

st.markdown("""
- 🟡 **Extra columns** are treated as enhancements (not breaking), shown in yellow above.  
- ✅ Core tabs and required columns must stay green for the Review Engine to work.  
- ❌ Any missing required column will break one or more pages and must be fixed immediately.
""")
