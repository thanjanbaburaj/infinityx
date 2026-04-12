from typing import Any, Dict

def is_exists(obj: Dict[str, Any]) -> bool:
    return bool(obj.get("exists"))

def get_message(obj: Dict[str, Any]) -> str:
    return str(obj.get("message", ""))
