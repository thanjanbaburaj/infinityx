# shared/utils.py
from datetime import datetime

def iso_to_date_str(value) -> str:
    if not value:
        return ""
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except Exception:
        return str(value)
