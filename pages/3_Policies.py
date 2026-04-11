import streamlit as st
import pandas as pd
from datetime import datetime
from utils.sheets import load_sheet, write_row, update_row

st.set_page_config(page_title="Policies", page_icon="📄", layout="wide")

# -----------------------------
# Helpers
# -----------------------------
def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def safe_float(v):
    try:
        return float(v) if v not in ["", None] else 0.0
    except:
        return 0.0

def safe_str(v):
    return "" if v is None else str(v)

POLICY_COLUMNS = [
    "PolicyID",
    "ClientID",
    "FullName",
    "Product",
    "Premium",
    "Frequency",
    "Status",
    "IssueDate",
    "PaidToDate",
    "NextPremiumDue",
    "CommissionRate",
    "ExpectedAnnualCommission",
    "LifeCover",
    "CICover",
    "DisabilityCover",
    "CurrentValue",
    "PolicyType",
    "Carrier",
    "PolicyNumber",
]

# -----------------------------
# Load data
# -----------------------------
st.title("📄 Policies")
st.caption("View and manage client policies (protection + investment).")

policies = load_sheet("Policies")
df_policies = pd.DataFrame(policies)

# Ensure all expected columns exist
for col in POLICY_COLUMNS:
    if col not in df_policies.columns:
        df_policies[col] = ""

clients = load_sheet("Clients")
df_clients = pd.DataFrame(clients)

client_map = {
    safe_str(row["ClientID"]): safe_str(row.get("FullName", ""))
    for _, row in df_clients.iterrows()
}

# -----------------------------
# Sidebar: Add / Edit selector
# -----------------------------
mode = st.sidebar.radio("Mode", ["View", "Add New Policy", "Edit Existing Policy"])

# -----------------------------
# VIEW MODE
# -----------------------------
if mode == "View":
    st.subheader("All Policies")

    if df_policies.empty:
        st.info("No policies found yet.")
    else:
        # Basic filters
        col1, col2 = st.columns(2)
        with col1:
            filter_client = st.selectbox(
                "Filter by Client",
                ["All"] + sorted(df_policies["FullName"].astype(str).unique().tolist()),
            )
        with col2:
            filter_carrier = st.selectbox(
                "Filter by Carrier",
                ["All"] + sorted(df_policies["Carrier"].astype(str).unique().tolist()),
            )

        df_view = df_policies.copy()

        if filter_client != "All":
            df_view = df_view[df_view["FullName"].astype(str) == filter_client]

        if filter_carrier != "All":
            df_view = df_view[df_view["Carrier"].astype(str) == filter_carrier]

        st.dataframe(
            df_view[
                [
                    "PolicyID",
                    "ClientID",
                    "FullName",
                    "Carrier",
                    "Product",
                    "PolicyNumber",
                    "PolicyType",
                    "Premium",
                    "Frequency",
                    "LifeCover",
                    "CICover",
                    "DisabilityCover",
                    "CurrentValue",
                    "Status",
                ]
            ].sort_values("FullName"),
            use_container_width=True,
        )

# -----------------------------
# ADD NEW POLICY
# -----------------------------
elif mode == "Add New Policy":
    st.subheader("Add New Policy")

    col1, col2 = st.columns(2)

    with col1:
        client_id = st.selectbox(
            "Client",
            [""] + sorted(client_map.keys()),
            format_func=lambda cid: f"{cid} - {client_map.get(cid, '')}" if cid else "Select client",
        )
        full_name = client_map.get(client_id, "")
        carrier = st.text_input("Carrier (e.g., MetLife, Zurich)")
        product = st.text_input("Product Name")
        policy_number = st.text_input("Policy Number")
        policy_type = st.selectbox(
            "Policy Type",
            ["Protection", "Investment", "Protection + Investment"],
        )
        status = st.selectbox("Status", ["Active", "Lapsed", "Paid-up", "Cancelled"])

    with col2:
        premium = st.text_input("Premium Amount")
        frequency = st.selectbox("Premium Frequency", ["Monthly", "Quarterly", "Semi-Annual", "Annual"])
        issue_date = st.date_input("Issue Date")
        paid_to_date = st.date_input("Paid To Date")
        next_premium_due = st.date_input("Next Premium Due")
        commission_rate = st.text_input("Commission Rate (%)", value="0")
        expected_annual_commission = st.text_input("Expected Annual Commission", value="0")

    st.markdown("### Coverage & Value")

    col3, col4 = st.columns(2)
    with col3:
        life_cover = st.text_input("Life Cover (Sum Assured)", value="0")
        ci_cover = st.text_input("Critical Illness Cover", value="0")
    with col4:
        disability_cover = st.text_input("Disability Cover", value="0")
        current_value = st.text_input("Current Investment Value", value="0")

    if st.button("Save Policy", type="primary"):
        if not client_id:
            st.error("Please select a client.")
        elif not carrier or not product:
            st.error("Carrier and Product are required.")
        else:
            new_policy = {
                "PolicyID": f"POL-{int(datetime.now().timestamp())}",
                "ClientID": client_id,
                "FullName": full_name,
                "Product": product,
                "Premium": premium,
                "Frequency": frequency,
                "Status": status,
                "IssueDate": issue_date.isoformat(),
                "PaidToDate": paid_to_date.isoformat(),
                "NextPremiumDue": next_premium_due.isoformat(),
                "CommissionRate": commission_rate,
                "ExpectedAnnualCommission": expected_annual_commission,
                "LifeCover": life_cover,
                "CICover": ci_cover,
                "DisabilityCover": disability_cover,
                "CurrentValue": current_value,
                "PolicyType": policy_type,
                "Carrier": carrier,
                "PolicyNumber": policy_number,
            }

            write_row("Policies", new_policy)
            st.success("Policy saved successfully.")
            st.experimental_rerun()

# -----------------------------
# EDIT EXISTING POLICY
# -----------------------------
elif mode == "Edit Existing Policy":
    st.subheader("Edit Existing Policy")

    if df_policies.empty:
        st.info("No policies to edit.")
    else:
        policy_ids = df_policies["PolicyID"].tolist()
        selected_policy_id = st.selectbox("Select Policy", [""] + policy_ids)

        if selected_policy_id:
            row = df_policies[df_policies["PolicyID"] == selected_policy_id].iloc[0].to_dict()

            col1, col2 = st.columns(2)

            with col1:
                client_id = st.selectbox(
                    "Client",
                    [""] + sorted(client_map.keys()),
                    index=([""] + sorted(client_map.keys())).index(safe_str(row.get("ClientID", ""))) if safe_str(row.get("ClientID", "")) in client_map else 0,
                    format_func=lambda cid: f"{cid} - {client_map.get(cid, '')}" if cid else "Select client",
                )
                full_name = client_map.get(client_id, row.get("FullName", ""))
                carrier = st.text_input("Carrier", value=safe_str(row.get("Carrier", "")))
                product = st.text_input("Product Name", value=safe_str(row.get("Product", "")))
                policy_number = st.text_input("Policy Number", value=safe_str(row.get("PolicyNumber", "")))
                policy_type = st.selectbox(
                    "Policy Type",
                    ["Protection", "Investment", "Protection + Investment"],
                    index=["Protection", "Investment", "Protection + Investment"].index(
                        safe_str(row.get("PolicyType", "Protection"))
                    ),
                )
                status = st.selectbox(
                    "Status",
                    ["Active", "Lapsed", "Paid-up", "Cancelled"],
                    index=["Active", "Lapsed", "Paid-up", "Cancelled"].index(
                        safe_str(row.get("Status", "Active"))
                    ),
                )

            with col2:
                premium = st.text_input("Premium Amount", value=safe_str(row.get("Premium", "")))
                frequency = st.selectbox(
                    "Premium Frequency",
                    ["Monthly", "Quarterly", "Semi-Annual", "Annual"],
                    index=["Monthly", "Quarterly", "Semi-Annual", "Annual"].index(
                        safe_str(row.get("Frequency", "Monthly"))
                    ),
                )
                issue_date = st.text_input("Issue Date (YYYY-MM-DD)", value=safe_str(row.get("IssueDate", "")))
                paid_to_date = st.text_input("Paid To Date (YYYY-MM-DD)", value=safe_str(row.get("PaidToDate", "")))
                next_premium_due = st.text_input("Next Premium Due (YYYY-MM-DD)", value=safe_str(row.get("NextPremiumDue", "")))
                commission_rate = st.text_input("Commission Rate (%)", value=safe_str(row.get("CommissionRate", "0")))
                expected_annual_commission = st.text_input(
                    "Expected Annual Commission", value=safe_str(row.get("ExpectedAnnualCommission", "0"))
                )

            st.markdown("### Coverage & Value")

            col3, col4 = st.columns(2)
            with col3:
                life_cover = st.text_input("Life Cover (Sum Assured)", value=safe_str(row.get("LifeCover", "0")))
                ci_cover = st.text_input("Critical Illness Cover", value=safe_str(row.get("CICover", "0")))
            with col4:
                disability_cover = st.text_input("Disability Cover", value=safe_str(row.get("DisabilityCover", "0")))
                current_value = st.text_input("Current Investment Value", value=safe_str(row.get("CurrentValue", "0")))

            if st.button("Update Policy", type="primary"):
                updated_policy = {
                    "PolicyID": selected_policy_id,
                    "ClientID": client_id,
                    "FullName": full_name,
                    "Product": product,
                    "Premium": premium,
                    "Frequency": frequency,
                    "Status": status,
                    "IssueDate": issue_date,
                    "PaidToDate": paid_to_date,
                    "NextPremiumDue": next_premium_due,
                    "CommissionRate": commission_rate,
                    "ExpectedAnnualCommission": expected_annual_commission,
                    "LifeCover": life_cover,
                    "CICover": ci_cover,
                    "DisabilityCover": disability_cover,
                    "CurrentValue": current_value,
                    "PolicyType": policy_type,
                    "Carrier": carrier,
                    "PolicyNumber": policy_number,
                }

                update_row("Policies", "PolicyID", selected_policy_id, updated_policy)
                st.success("Policy updated successfully.")
                st.experimental_rerun()
