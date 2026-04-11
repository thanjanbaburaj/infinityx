import streamlit as st
from utils.sheets import get_worksheet

st.title("🔍 Header Debugger")

ws = get_worksheet("Clients")

raw_row1 = ws.row_values(1)
raw_row2 = ws.row_values(2)

st.write("### Row 1 (raw):")
st.write(raw_row1)

st.write("### Row 2 (raw):")
st.write(raw_row2)
