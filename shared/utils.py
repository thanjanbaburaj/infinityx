# shared/utils.py

from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime


def safe_get(d: Dict[str, Any], key: str, default: Any = "") -> Any:
    """
    Safely get a value from a dict, returning default if key is missing or value is None.
    """
    if not isinstance(d, dict):
        return default
    value = d.get(key, default)
    return default if value is None else value


def normalize_phone(phone: str) -> str:
    """
    Very light normalization for phone numbers.
    You can extend this later with country codes, formatting, etc.
    """
    if not phone:
        return ""
    return "".join(ch for ch in str(phone) if ch.isdigit() or ch == "+")


def format_currency(value: Any, currency: str = "AED") -> str:
    """
    Simple currency formatter.
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        return ""
    return f"{currency} {num:,.2f}"


def parse_date(value: Any, fmt_in: str = "%Y-%m-%d", fmt_out: str = "%d-%b-%Y") -> str:
    """
    Parse a date string and reformat it.
    """
    if not value:
        return ""
    if isinstance(value, datetime):
        return value.strftime(fmt_out)
    try:
        dt = datetime.strptime(str(value), fmt_in)
        return dt.strftime(fmt_out)
    except ValueError:
        return str(value)
