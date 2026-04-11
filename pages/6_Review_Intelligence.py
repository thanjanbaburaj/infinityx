# -----------------------------
# Load Clients (Safe Loader)
# -----------------------------
clients = load_sheet("Clients")  # MUST MATCH EXACT TAB NAME
df_clients = pd.DataFrame(clients)

# Debug: Show columns if something is wrong
if df_clients.empty:
    st.error("❌ ERROR: 'Clients' sheet is empty or not loading. Check Google Sheet tab name.")
    st.stop()

expected_cols = ["ClientID", "FullName"]
missing = [c for c in expected_cols if c not in df_clients.columns]

if missing:
    st.error(f"❌ ERROR: Missing required columns in 'Clients' sheet: {missing}\n\n"
             f"Found columns: {list(df_clients.columns)}")
    st.stop()

client_ids = df_clients["ClientID"].tolist()
