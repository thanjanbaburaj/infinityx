# console/pages/7_Backend_Health.py

import sys
from pathlib import Path
import traceback

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared import read_records  # type: ignore


st.set_page_config(page_title="Backend Health", page_icon="🩺", layout="wide")


def main():
    st.title("Backend Health Dashboard")

    st.write("Quick checks to ensure Sheets + Apps Script are responding correctly.")

    checks = {
        "CLIENTS": False,
        "LEADS": False,
        "MEETINGS": False,
        "REFERRALS": False,
        "POLICIES": False,
    }

    errors = {}

    for sheet in checks.keys():
        try:
            rows = read_records(sheet)
            checks[sheet] = True
            st.success(f"{sheet}: OK ({len(rows)} rows)")
        except Exception as e:
            checks[sheet] = False
            errors[sheet] = str(e)
            st.error(f"{sheet}: ERROR")

    if errors:
        st.markdown("---")
        st.subheader("Error Details")
        for sheet, err in errors.items():
            with st.expander(f"{sheet} error"):
                st.code(err)
                st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
