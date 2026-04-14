# clientview/components/layout.py

import streamlit as st


def section(title: str, subtitle: str | None = None):
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)
