# shared/sheets.py
import requests
import streamlit as st

@st.cache_data(show_spinner=False)
def get_gas_base_url() -> str:
    url = st.secrets.get("GAS_BASE_URL", "").strip()
    if not url:
        raise RuntimeError("GAS_BASE_URL missing in .streamlit/secrets.toml")
    return url

def _post(payload: dict, retries: int = 1):
    base_url = get_gas_base_url()
    last_err = None
    for _ in range(retries):
        try:
            resp = requests.post(base_url, json=payload, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("success", False):
                raise RuntimeError(f"GAS error: {data.get('error')}")
            return data
        except Exception as e:
            last_err = e
    raise RuntimeError(f"GAS request failed after {retries} attempts: {last_err}")

def read_rows(sheet: str, filters: dict | None = None) -> list[dict]:
    payload = {
        "action": "read",
        "sheet": sheet,
        "filters": filters or {}
    }
    data = _post(payload)
    return data.get("rows", [])

def create_row(sheet: str, data: dict) -> dict:
    payload = {
        "action": "create",
        "sheet": sheet,
        "data": data
    }
    return _post(payload)

def update_row(sheet: str, key: str, value, data: dict) -> dict:
    payload = {
        "action": "update",
        "sheet": sheet,
        "key": key,
        "value": value,
        "data": data
    }
    return _post(payload)

def delete_row(sheet: str, key: str, value) -> dict:
    payload = {
        "action": "delete",
        "sheet": sheet,
        "key": key,
        "value": value
    }
    return _post(payload)
