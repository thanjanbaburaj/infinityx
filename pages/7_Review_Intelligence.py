import streamlit as st
import pandas as pd
from utils.sheets import load_sheet
import math
from datetime import date

st.set_page_config(page_title="Review Meeting Assistant", page_icon="🧭", layout="wide")

st.title("🧭 Infinity‑X Review Meeting Assistant")
st.caption("Guided, intelligent review flow: snapshot → gaps → architecture → blueprint → opportunities.")

# -----------------------------
# Helpers
# -----------------------------
def fv(amount, rate, years):
    return amount * ((1 + rate) ** years)

def retirement_corpus(target_monthly, years_to_retire, years_in_retirement=25, inflation=0.03):
    future_monthly = fv(target_monthly, inflation, years_to_retire)
    return future_monthly * 12 * years_in_retirement

def education_target_per_child(current_annual_cost, years_to_university, edu_inflation=0.06, years_of_study=4):
    future_annual = fv(current_annual_cost, edu_inflation, years_to_university)
    return future_annual * years_of_study

def safe_get(row, key, default=0.0):
    try:
        v = row.get(key, default)
        if v in ["", None]:
            return default
        return float(v)
    except Exception:
        return default

def safe_int(v, default=0):
    try:
        if v in ["", None]:
            return default
        return int(v)
    except Exception:
        return default

# -----------------------------
# Load data
# -----------------------------
st.sidebar.header("Client Selection")

try:
    records = load_sheet("Financial_Fact_Find")
    df = pd.DataFrame(records)
except Exception as e:
    st.error("Failed to load Financial_Fact_Find from Google Sheets.")
    st.code(str(e))
    st.stop()

if df.empty:
    st.warning("No fact‑find data found.")
    st.stop()

id_col_candidates = [c for c in df.columns if c.lower() in ["clientid", "client_id", "id"]]
name_col_candidates = [c for c in df.columns if "name" in c.lower()]

client_id_col = id_col_candidates[0] if id_col_candidates else df.columns[0]
client_name_col = name_col_candidates[0] if name_col_candidates else df.columns[0]

df["__label__"] = df[client_name_col].astype(str) + " (" + df[client_id_col].astype(str) + ")"

selected_label = st.sidebar.selectbox("Select client", df["__label__"].tolist())
client_row = df[df["__label__"] == selected_label].iloc[0].to_dict()

st.sidebar.markdown(f"**Selected:** {client_row.get(client_name_col, '')}")
st.sidebar.markdown(f"**Client ID:** {client_row.get(client_id_col, '')}")

# -----------------------------
# 1) Snapshot
# -----------------------------
st.header("1️⃣ Snapshot")

col1, col2, col3, col4 = st.columns(4)

income = safe_get(client_row, "MonthlyIncome", 0)
expenses = safe_get(client_row, "MonthlyExpenses", 0)
assets = safe_get(client_row, "TotalAssets", 0)
liabilities = safe_get(client_row, "TotalLiabilities", 0)

dependents = safe_int(client_row.get("Dependents", 0))
retirement_age = safe_int(client_row.get("RetirementAge", 60))
current_age = safe_int(client_row.get("Age", 40))

surplus = income - expenses
net_worth = assets - liabilities
years_to_retire = max(retirement_age - current_age, 0)
dependency_ratio = (dependents / max(1, current_age)) if current_age > 0 else 0

with col1:
    st.metric("Monthly Income", f"AED {income:,.0f}")
with col2:
    st.metric("Monthly Expenses", f"AED {expenses:,.0f}", delta=f"AED {surplus:,.0f} surplus")
with col3:
    st.metric("Net Worth", f"AED {net_worth:,.0f}")
with col4:
    st.metric("Dependents", dependents)

st.markdown("—")

# -----------------------------
# 2) Gap Engine
# -----------------------------
st.header("2️⃣ Gap Analysis")

# Inputs (fallbacks)
existing_life_cover = safe_get(client_row, "ExistingLifeCover", 0)
existing_ci_cover = safe_get(client_row, "ExistingCICover", 0)
liabilities_total = liabilities
liquid_assets = safe_get(client_row, "LiquidAssets", 0)
retirement_assets = safe_get(client_row, "RetirementAssets", 0)
current_edu_cost = safe_get(client_row, "CurrentAnnualEduCost", 80000)

# Children ages (optional columns)
child1_age = safe_int(client_row.get("Child1Age", 0))
child2_age = safe_int(client_row.get("Child2Age", 0))
child3_age = safe_int(client_row.get("Child3Age", 0))

# Life cover gap
life_target = (income * 12 * 10) + liabilities_total
life_gap = max(life_target - existing_life_cover, 0)

# Income protection gap (10 years)
income_protection_target = income * 12 * 10

# CI gap
ci_target = income * 5
ci_gap = max(ci_target - existing_ci_cover, 0)

# Emergency fund gap (6 months)
emergency_target = expenses * 6
emergency_gap = max(emergency_target - liquid_assets, 0)

# Retirement gap
ret_target_monthly = income * 0.7
ret_corpus = retirement_corpus(ret_target_monthly, years_to_retire, years_in_retirement=25, inflation=0.03)
ret_gap = max(ret_corpus - retirement_assets, 0)

# Education gap
edu_targets = []
for age in [child1_age, child2_age, child3_age]:
    if age > 0 and age < 25:
        years_to_uni = max(18 - age, 0)
        if years_to_uni > 0:
            edu_targets.append(education_target_per_child(current_edu_cost, years_to_uni, edu_inflation=0.06, years_of_study=4))

edu_total_target = sum(edu_targets)
edu_existing = safe_get(client_row, "EducationSavings", 0)
edu_gap = max(edu_total_target - edu_existing, 0)

gap_col1, gap_col2, gap_col3 = st.columns(3)

with gap_col1:
    st.metric("Life Cover Gap", f"AED {life_gap:,.0f}")
    st.metric("Income Protection Target (10 yrs)", f"AED {income_protection_target:,.0f}")
    st.metric("CI Gap", f"AED {ci_gap:,.0f}")

with gap_col2:
    st.metric("Emergency Fund Gap", f"AED {emergency_gap:,.0f}")
    st.metric("Retirement Corpus Target", f"AED {ret_corpus:,.0f}")
    st.metric("Retirement Gap", f"AED {ret_gap:,.0f}")

with gap_col3:
    st.metric("Education Target (All Children)", f"AED {edu_total_target:,.0f}")
    st.metric("Education Gap", f"AED {edu_gap:,.0f}")
    st.metric("Years to Retirement", years_to_retire)

st.markdown("—")

# -----------------------------
# 3) Architecture (Must / Should / Could)
# -----------------------------
st.header("3️⃣ Financial Architecture")

must_items = []
should_items = []
could_items = []

if life_gap > 0:
    must_items.append(f"Life cover gap of AED {life_gap:,.0f}")
if emergency_gap > 0:
    must_items.append(f"Emergency fund gap of AED {emergency_gap:,.0f}")
if income_protection_target > 0:
    must_items.append(f"Income protection for 10 years of income")

if ci_gap > 0:
    should_items.append(f"Critical illness gap of AED {ci_gap:,.0f}")
if edu_gap > 0:
    should_items.append(f"Education funding gap of AED {edu_gap:,.0f}")
if ret_gap > 0:
    should_items.append(f"Retirement gap of AED {ret_gap:,.0f}")

could_items.append("Wealth accumulation / investment plan once core gaps are addressed")
could_items.append("Legacy / estate planning")
could_items.append("Optional riders and enhancements")

arch_col1, arch_col2, arch_col3 = st.columns(3)

with arch_col1:
    st.subheader("MUST")
    if must_items:
        for item in must_items:
            st.write(f"• {item}")
    else:
        st.write("• Core protection looks reasonably covered.")

with arch_col2:
    st.subheader("SHOULD")
    if should_items:
        for item in should_items:
            st.write(f"• {item}")
    else:
        st.write("• No major secondary gaps detected.")

with arch_col3:
    st.subheader("COULD")
    for item in could_items:
        st.write(f"• {item}")

st.markdown("—")

# -----------------------------
# 4) Proposal tiers (Minimum / Ideal / Accelerated)
# -----------------------------
st.header("4️⃣ Proposal Tiers (Indicative)")

# Simple indicative logic (you can refine later)
life_min = life_gap * 0.4
life_ideal = life_gap * 0.7
life_acc = life_gap

ci_min = ci_gap * 0.4
ci_ideal = ci_gap * 0.7
ci_acc = ci_gap

ret_min_monthly = ret_gap / max(years_to_retire * 12 * 1.5, 1)
ret_ideal_monthly = ret_gap / max(years_to_retire * 12, 1)
ret_acc_monthly = ret_gap / max(years_to_retire * 12 * 0.7, 1)

edu_min_monthly = edu_gap / max(10 * 12, 1)
edu_ideal_monthly = edu_gap / max(8 * 12, 1)
edu_acc_monthly = edu_gap / max(5 * 12, 1)

tier_col1, tier_col2, tier_col3 = st.columns(3)

with tier_col1:
    st.subheader("Minimum")
    st.write(f"Life cover: AED {life_min:,.0f}")
    st.write(f"CI cover: AED {ci_min:,.0f}")
    st.write(f"Retirement saving: ~AED {ret_min_monthly:,.0f}/month")
    st.write(f"Education saving: ~AED {edu_min_monthly:,.0f}/month")
    st.caption("For clients who want to start with essentials at a lower commitment.")

with tier_col2:
    st.subheader("Ideal")
    st.write(f"Life cover: AED {life_ideal:,.0f}")
    st.write(f"CI cover: AED {ci_ideal:,.0f}")
    st.write(f"Retirement saving: ~AED {ret_ideal_monthly:,.0f}/month")
    st.write(f"Education saving: ~AED {edu_ideal_monthly:,.0f}/month")
    st.caption("Balanced protection and savings — most clients choose this tier.")

with tier_col3:
    st.subheader("Accelerated")
    st.write(f"Life cover: AED {life_acc:,.0f}")
    st.write(f"CI cover: AED {ci_acc:,.0f}")
    st.write(f"Retirement saving: ~AED {ret_acc_monthly:,.0f}/month")
    st.write(f"Education saving: ~AED {edu_acc_monthly:,.0f}/month")
    st.caption("For clients who want to close gaps aggressively and build wealth faster.")

st.markdown("—")

# -----------------------------
# 5) Blueprint Summary + WhatsApp text
# -----------------------------
st.header("5️⃣ Blueprint Summary")

summary_lines = []

summary_lines.append(f"Client: {client_row.get(client_name_col, '')} (ID: {client_row.get(client_id_col, '')})")
summary_lines.append("")
summary_lines.append("Current Snapshot:")
summary_lines.append(f"• Monthly income: AED {income:,.0f}")
summary_lines.append(f"• Monthly expenses: AED {expenses:,.0f}")
summary_lines.append(f"• Net worth: AED {net_worth:,.0f}")
summary_lines.append(f"• Dependents: {dependents}")
summary_lines.append("")
summary_lines.append("Gaps Identified:")
summary_lines.append(f"• Life cover gap: AED {life_gap:,.0f}")
summary_lines.append(f"• CI gap: AED {ci_gap:,.0f}")
summary_lines.append(f"• Emergency fund gap: AED {emergency_gap:,.0f}")
summary_lines.append(f"• Retirement gap: AED {ret_gap:,.0f}")
summary_lines.append(f"• Education gap: AED {edu_gap:,.0f}")
summary_lines.append("")
summary_lines.append("Priority Areas (MUST / SHOULD):")
for item in must_items:
    summary_lines.append(f"• MUST: {item}")
for item in should_items:
    summary_lines.append(f"• SHOULD: {item}")
summary_lines.append("")
summary_lines.append("Indicative Plan (Ideal Tier):")
summary_lines.append(f"• Life cover: AED {life_ideal:,.0f}")
summary_lines.append(f"• CI cover: AED {ci_ideal:,.0f}")
summary_lines.append(f"• Retirement saving: ~AED {ret_ideal_monthly:,.0f}/month")
summary_lines.append(f"• Education saving: ~AED {edu_ideal_monthly:,.0f}/month")
summary_lines.append("")
summary_lines.append("Next Steps:")
summary_lines.append("• Review options together")
summary_lines.append("• Confirm priorities")
summary_lines.append("• Implement protection and savings plan")

blueprint_text = "\n".join(summary_lines)

st.text_area("Blueprint (copy to WhatsApp / email)", blueprint_text, height=260)

st.info("Use this blueprint as your spoken summary and as a follow‑up message after the meeting.")

# -----------------------------
# 6) Opportunity / Referral prompts
# -----------------------------
st.header("6️⃣ Opportunities & Referrals")

opp_col1, opp_col2 = st.columns(2)

with opp_col1:
    st.subheader("Advisor Talking Points")
    st.write("• “Based on your situation, these are the 2–3 areas I’d prioritise first…”")
    st.write("• “Between protection, retirement, and education, which feels most important to fix now?”")
    st.write("• “Would you be more comfortable starting with the Minimum or Ideal plan?”")

with opp_col2:
    st.subheader("Referral Prompt")
    st.write("• “If you know 1–2 families who would benefit from a review like this, I’d be happy to help them as well.”")
    st.write("• “You’ve done something important today — most people never get this clarity.”")
