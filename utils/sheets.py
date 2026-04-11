import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from functools import lru_cache

# -----------------------------
# CONFIG
# -----------------------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SPREADSHEET_NAME = "Infinity-X Backend"  # MUST match your Google Sheet title


# -----------------------------
# AUTH & CLIENT
# -----------------------------
@st.cache_resource(show_spinner=False)
def get_gspread_client():
    service_account_info = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client


@st.cache_resource(show_spinner=False)
def get_spreadsheet():
    client = get_gspread_client()
    return client.open(SPREADSHEET_NAME)


# -----------------------------
# CORE HELPERS
# -----------------------------
def get_worksheet(tab_name: str):
    ss = get_spreadsheet()
    try:
        return ss.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        st.error(f"❌ Worksheet '{tab_name}' not found in '{SPREADSHEET_NAME}'.")
        raise


def load_sheet(tab_name: str):
    ws = get_worksheet(tab_name)
    records = ws.get_all_records()
    return records


def write_row(tab_name: str, row_dict: dict):
    ws = get_worksheet(tab_name)
    headers = ws.row_values(1)

    # Ensure all keys exist in headers
    for key in row_dict.keys():
        if key not in headers:
            headers.append(key)

    # Rewrite header row if extended
    ws.update("1:1", [headers])

    # Build row in header order
    row = [row_dict.get(h, "") for h in headers]
    ws.append_row(row, value_input_option="USER_ENTERED")


def update_row(tab_name: str, key_column: str, key_value: str, updated_dict: dict):
    ws = get_worksheet(tab_name)
    data = ws.get_all_records()
    headers = ws.row_values(1)

    # Find row index (1-based, including header)
    row_index = None
    for i, row in enumerate(data, start=2):  # data starts at row 2
        if str(row.get(key_column, "")) == str(key_value):
            row_index = i
            break

    if row_index is None:
        st.error(f"❌ Row with {key_column} = {key_value} not found in '{tab_name}'.")
        return

    # Ensure all keys exist in headers
    for key in updated_dict.keys():
        if key not in headers:
            headers.append(key)

    # Rewrite header row if extended
    ws.update("1:1", [headers])

    # Build row in header order
    row_values = [updated_dict.get(h, "") for h in headers]
    ws.update(f"{row_index}:{row_index}", [row_values])


# -----------------------------
# CONVENIENCE: LOAD CLIENTS
# -----------------------------
def load_clients():
    return load_sheet("Clients")
