# console/components/layout.py

import streamlit as st


def two_column_layout():
    return st.columns([2, 3])


def section_header(title: str, subtitle: str | None = None):
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)
