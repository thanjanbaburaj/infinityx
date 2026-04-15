# shared/utils.py
import streamlit as st
from datetime import datetime

def iso_to_date_str(value: str | None) -> str:
    if not value:
        return ""
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except Exception:
        return str(value)

def info_box(title: str, body: str):
    st.markdown(f"**{title}**")
    st.write(body)
