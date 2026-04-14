# shared/auth.py

import os


class AuthError(Exception):
    pass


def get_api_token() -> str:
    """
    Returns the API token used to authenticate with the Apps Script backend.
    Reads from environment or Streamlit secrets.
    """
    token = os.getenv("GAS_API_TOKEN") or os.environ.get("GAS_API_TOKEN")
    if not token:
        raise AuthError("GAS_API_TOKEN not set in environment or secrets.")
    return token
