import os
import streamlit as st

def get_apps_script_base_url() -> str:
    return st.secrets["backend"]["apps_script_base_url"]

def get_sheet_id() -> str:
    return st.secrets["backend"]["sheet_id"]

def get_console_password() -> str:
    return st.secrets["auth"]["console_password"]

def get_clientview_password() -> str:
    return st.secrets["auth"]["clientview_password"]
