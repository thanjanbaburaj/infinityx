import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

@st.cache_resource
def get_client():
    # Load service account credentials from TOML
    info = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(info, SCOPE)
    return gspread.authorize(creds)

def load_sheet(tab_name):
    # Open Google Sheet using spreadsheet_id from TOML
    gc = get_client()
    sh = gc.open_by_key(st.secrets["spreadsheet_id"])
    ws = sh.worksheet(tab_name)
    return ws.get_all_records()

def append_row(tab_name, row_values):
    # Append a row to a specific tab
    gc = get_client()
    sh = gc.open_by_key(st.secrets["spreadsheet_id"])
    ws = sh.worksheet(tab_name)
    ws.append_row(row_values)
