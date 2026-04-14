# shared/sheets.py

import os
import time
import json
from typing import Any, Dict, List, Optional

import requests


class SheetsAPIError(Exception):
    pass


def _get_base_url() -> str:
    base_url = os.getenv("GAS_BASE_URL") or os.environ.get("GAS_BASE_URL")
    if not base_url:
        raise SheetsAPIError("GAS_BASE_URL not set in environment or secrets.")
    return base_url.rstrip("/")


def _get_api_token() -> str:
    token = os.getenv("GAS_API_TOKEN") or os.environ.get("GAS_API_TOKEN")
    if not token:
        raise SheetsAPIError("GAS_API_TOKEN not set in environment or secrets.")
    return token


def _post(payload: Dict[str, Any], max_retries: int = 3, backoff: float = 0.8) -> Dict[str, Any]:
    """
    Core POST helper with simple retry for write operations.
    """
    url = _get_base_url()
    token = _get_api_token()

    payload_with_token = {**payload, "token": token}

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(url, json=payload_with_token, timeout=15)
            if resp.status_code != 200:
                raise SheetsAPIError(f"GAS HTTP {resp.status_code}: {resp.text}")

            data = resp.json()
            if not data.get("success", False):
                raise SheetsAPIError(f"GAS error: {data.get('error', 'Unknown error')}")

            return data

        except (requests.RequestException, SheetsAPIError) as e:
            if attempt == max_retries:
                raise SheetsAPIError(f"GAS request failed after {max_retries} attempts: {e}")
            time.sleep(backoff * attempt)

    # Should never reach here
    raise SheetsAPIError("Unexpected error in _post")


# ---------- PUBLIC CRUD HELPERS ----------

def create_record(sheet: str, data: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "action": "create",
        "sheet": sheet,
        "data": data,
    }
    return _post(payload)


def read_records(
    sheet: str,
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    payload = {
        "action": "read",
        "sheet": sheet,
        "filters": filters or {},
    }
    result = _post(payload, max_retries=1)  # read usually doesn't need retries
    return result.get("rows", [])


def update_record(
    sheet: str,
    key: str,
    value: Any,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    payload = {
        "action": "update",
        "sheet": sheet,
        "key": key,
        "value": value,
        "data": data,
    }
    return _post(payload)


def delete_record(
    sheet: str,
    key: str,
    value: Any
) -> Dict[str, Any]:
    payload = {
        "action": "delete",
        "sheet": sheet,
        "key": key,
        "value": value,
    }
    return _post(payload)
