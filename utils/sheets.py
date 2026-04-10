import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

@st.cache_resource
def get_client():
    raw = st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"]
    info = json.loads(raw)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(info, SCOPE)
    return gspread.authorize(creds)

def load_sheet(sheet_name, tab):
    gc = get_client()
    ws = gc.open(sheet_name).worksheet(tab)
    return ws.get_all_records()

def append_row(sheet_name, tab, row):
    gc = get_client()
    ws = gc.open(sheet_name).worksheet(tab)
    ws.append_row(row)
