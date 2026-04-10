from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ReviewMeetingData:
    client_id: str
    client_name: str
    meeting_datetime: str
    life_changes: str
    new_goals: str
    upcoming_decisions: str
    current_architecture_notes: str
    gap_insights: str
    upgrade_option_chosen: str
    upgrade_notes: str
    referral_names: str
    referral_context: str
    follow_up_actions: str

def create_review_summary(data: ReviewMeetingData) -> str:
    d = asdict(data)
    lines = [
        f"Infinity-X Review Summary for {d['client_name']} ({d['client_id']})",
        f"Meeting Time: {d['meeting_datetime']}",
        "",
        "1) Life Update Scan",
        f"- Life changes: {d['life_changes']}",
        f"- New goals/responsibilities: {d['new_goals']}",
        f"- Upcoming financial decisions: {d['upcoming_decisions']}",
        "",
        "2) Current Architecture",
        f"- Notes: {d['current_architecture_notes']}",
        "",
        "3) Gap Check",
        f"- Key insights: {d['gap_insights']}",
        "",
        "4) Micro-Upgrade",
        f"- Option chosen (Must/Should/Could/None): {d['upgrade_option_chosen']}",
        f"- Notes: {d['upgrade_notes']}",
        "",
        "5) Referrals",
        f"- Names / relationships: {d['referral_names']}",
        f"- Context: {d['referral_context']}",
        "",
        "6) Follow-Up",
        f"- Actions: {d['follow_up_actions']}",
        "",
        "Generated via Infinity-X Review Framework."
    ]
    return "\n".join(lines)

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M")
