import requests
from typing import Any, Dict
from shared import config

BASE_URL = config.get_apps_script_base_url()

def call_backend(action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = BASE_URL
    data = {
        "action": action,
        "payload": payload,
    }
    resp = requests.post(url, json=data, timeout=15)
    resp.raise_for_status()
    return resp.json()

def get_review_summary(client_id: str) -> Dict[str, Any]:
    return call_backend("buildReviewSummary", {"client_id": client_id})

def get_whatsapp_summary(client_id: str) -> Dict[str, Any]:
    return call_backend("buildWhatsAppSummary", {"client_id": client_id})

def get_follow_up(client_id: str) -> Dict[str, Any]:
    return call_backend("buildFollowUp", {"client_id": client_id})
