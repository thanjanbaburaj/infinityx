import streamlit as st
import pandas as pd
from datetime import datetime
from utils.sheets import load_sheet

st.set_page_config(page_title="Review Intelligence", page_icon="🧠", layout="wide")

# -----------------------------
# Helpers
# -----------------------------
def safe_float(v):
    try:
        return float(v) if v not in ["", None] else 0.0
    except:
        return 0.0


def safe_int(v):
    try:
        return int(v) if v not in ["", None] else 0
    except:
        return 0


def fv(amount, rate, years):
    return amount * ((1 + rate) ** years)


def now_str():
    return datetime.now().strftime("%d %b %Y, %I:%M %p")


# -----------------------------
# Page Title
# -----------------------------
st.title("🧠 Review Intelligence Engine")
st.caption("Advisor-only intelligence: snapshot → gaps → architecture → proposal → blueprint")

# -----------------------------
# Load Clients (safe)
# -----------------------------
clients = load_sheet("Clients")
df_clients = pd.DataFrame(clients)

if df_clients.empty:
    st.error("❌ 'Clients' sheet is empty or not loading. Check Google Sheet.")
    st.stop()

expected_client_cols = ["ClientID", "FullName"]
missing_client_cols = [c for c in expected_client_cols if c not in df_clients.columns]

if missing_client_cols:
    st.error(
        f"❌ Missing required columns in 'Clients' sheet: {missing_client_cols}\n\n"
        f"Found columns: {list(df_clients.columns)}"
    )
    st.stop()

client_ids = df_clients["ClientID"].tolist()
client_id = st.selectbox("Select Client", [""] + client_ids)

if not client_id:
    st.info("Select a client to continue.")
    st.stop()

client_row = df_clients[df_clients["ClientID"] == client_id].iloc[0].to_dict()
client_name = client_row.get("FullName", "")

st.markdown(f"### Client: **{client_name}**")

# -----------------------------
# Load Fact Find
# -----------------------------
fact = load_sheet("Financial_Fact_Find")
df_fact = pd.DataFrame(fact)

if df_fact.empty:
    st.error("❌ 'Financial_Fact_Find' sheet is empty or not loading.")
    st.stop()

ff_match = df_fact[df_fact["ClientID"].astype(str) == str(client_id)]
if ff_match.empty:
    st.error("No Fact Find data found for this client.")
    st.stop()

ff = ff_match.iloc[0].to_dict()

income = safe_float(ff.get("Income"))
expenses = safe_float(ff.get("Expenses"))
assets = safe_float(ff.get("Assets"))
liabilities = safe_float(ff.get("Liabilities"))
dependents = safe_int(ff.get("Dependents"))
ret_age = safe_int(ff.get("RetirementAge"))
current_age = safe_int(ff.get("Age", 40))
years_to_retire = max(ret_age - current_age, 0)

# -----------------------------
# Load Policies
# -----------------------------
policies = load_sheet("Policies")
df_policies = pd.DataFrame(policies)

if df_policies.empty:
    client_policies = []
else:
    client_policies = [
        p for _, p in df_policies.iterrows()
        if str(p.get("ClientID", "")) == str(client_id)
    ]

existing_life = sum(safe_float(p.get("LifeCover")) for p in client_policies)
existing_ci = sum(safe_float(p.get("CICover")) for p in client_policies)
existing_disability = sum(safe_float(p.get("DisabilityCover")) for p in client_policies)
existing_investments = sum(safe_float(p.get("CurrentValue")) for p in client_policies)

# -----------------------------
# Snapshot
# -----------------------------
st.header("1️⃣ Snapshot")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Income", f"AED {income:,.0f}")
col2.metric("Expenses", f"AED {expenses:,.0f}", delta=f"AED {income - expenses:,.0f} surplus")
col3.metric("Assets", f"AED {assets:,.0f}")
col4.metric("Liabilities", f"AED {liabilities:,.0f}")

st.markdown("---")

# -----------------------------
# Gap Engine
# -----------------------------
st.header("2️⃣ Gap Analysis")

# Life cover gap
life_target = (income * 12 * 10) + liabilities
life_gap = max(life_target - existing_life, 0)

# CI gap
ci_target = income * 5
ci_gap = max(ci_target - existing_ci, 0)

# Emergency fund
emergency_target = expenses * 6
emergency_gap = max(emergency_target - assets, 0)

# Retirement gap
target_monthly = income * 0.7
future_monthly = fv(target_monthly, 0.03, years_to_retire)
ret_corpus = future_monthly * 12 * 25
ret_gap = max(ret_corpus - existing_investments, 0)

col1, col2, col3 = st.columns(3)
col1.metric("Life Cover Gap", f"AED {life_gap:,.0f}")
col1.metric("CI Gap", f"AED {ci_gap:,.0f}")
col2.metric("Emergency Gap", f"AED {emergency_gap:,.0f}")
col2.metric("Retirement Corpus", f"AED {ret_corpus:,.0f}")
col3.metric("Retirement Gap", f"AED {ret_gap:,.0f}")
col3.metric("Existing Investments", f"AED {existing_investments:,.0f}")

st.markdown("---")

# -----------------------------
# Architecture
# -----------------------------
st.header("3️⃣ Architecture (MUST / SHOULD / COULD)")

must = []
should = []
could = ["Wealth accumulation", "Legacy planning"]

if life_gap > 0:
    must.append(f"Life cover gap: AED {life_gap:,.0f}")
if emergency_gap > 0:
    must.append(f"Emergency fund gap: AED {emergency_gap:,.0f}")

if ci_gap > 0:
    should.append(f"Critical illness gap: AED {ci_gap:,.0f}")
if ret_gap > 0:
    should.append(f"Retirement gap: AED {ret_gap:,.0f}")

col1, col2, col3 = st.columns(3)
col1.subheader("MUST")
for m in must:
    col1.write(f"• {m}")

col2.subheader("SHOULD")
for s in should:
    col2.write(f"• {s}")

col3.subheader("COULD")
for c in could:
    col3.write(f"• {c}")

st.markdown("---")

# -----------------------------
# Proposal Tiers
# -----------------------------
st.header("4️⃣ Proposal Options")

life_min = life_gap * 0.4
life_ideal = life_gap * 0.7
life_acc = life_gap

ci_min = ci_gap * 0.4
ci_ideal = ci_gap * 0.7
ci_acc = ci_gap

col1, col2, col3 = st.columns(3)

col1.subheader("Minimum")
col1.write(f"Life: AED {life_min:,.0f}")
col1.write(f"CI: AED {ci_min:,.0f}")

col2.subheader("Ideal")
col2.write(f"Life: AED {life_ideal:,.0f}")
col2.write(f"CI: AED {ci_ideal:,.0f}")

col3.subheader("Accelerated")
col3.write(f"Life: AED {life_acc:,.0f}")
col3.write(f"CI: AED {ci_acc:,.0f}")

st.markdown("---")

# -----------------------------
# Blueprint Summary
# -----------------------------
st.header("5️⃣ Blueprint Summary")

summary = f"""
Client: {client_name}

MUST:
{chr(10).join(must) if must else 'None'}

SHOULD:
{chr(10).join(should) if should else 'None'}

COULD:
{chr(10).join(could)}

Proposal (Ideal):
Life: AED {life_ideal:,.0f}
CI: AED {ci_ideal:,.0f}

Existing Investments: AED {existing_investments:,.0f}
"""

st.text_area("Copy Summary", summary, height=300)
