def money(aed: float) -> str:
    try:
        return f"AED {aed:,.0f}"
    except Exception:
        return f"AED {aed}"
