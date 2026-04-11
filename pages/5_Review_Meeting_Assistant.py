import streamlit as st
from utils.sheets import init_sheets, load_clients
from utils.review_framework import ReviewMeetingData, create_review_summary, now_str

st.set_page_config(page_title="Review Meeting Assistant", page_icon="🧾", layout="wide")

@st.cache_resource
def get_client():
    return init_sheets()

def main():
    st.title("Infinity-X Review Meeting Assistant")

    client = get_client()
    clients_df = load_clients(client)

    col_top1, col_top2 = st.columns([2, 1])
    with col_top1:
        st.markdown("Use this during your review meetings to stay structured, premium, and referral-ready.")
    with col_top2:
        st.write(f"Now: {now_str()}")

    # --- Client selection ---
    st.subheader("Client Selection")
    client_id = st.text_input("ClientID")
    client_name = st.text_input("Client Name")

    if clients_df is not None and not clients_df.empty and not client_id and st.checkbox("Pick from Clients list"):
        ids = clients_df["ClientID"].tolist()
        selected = st.selectbox("Select ClientID", [""] + ids)
        if selected:
            client_id = selected
            row = clients_df[clients_df["ClientID"] == selected].iloc[0]
            if not client_name:
                client_name = row.get("FullName", "")

    if not client_id:
        st.info("Enter or select a ClientID to proceed.")
        return

    meeting_time = st.text_input("Meeting Time", value=now_str())

    st.markdown("---")

    # --- Step 1: Life Update Scan ---
    st.subheader("1. Life Update Scan")
    life_changes = st.text_area("What’s changed in your life since we last spoke?")
    new_goals = st.text_area("Any new goals or responsibilities?")
    upcoming_decisions = st.text_area("Any financial decisions coming up this year?")

    st.markdown("---")

    # --- Step 2 & 3: Architecture + Gap Notes (you’ll use ClientView visuals) ---
    st.subheader("2. Current Architecture (Notes)")
    st.caption("Use Architecture / Gap Engine on ClientView for visuals; capture key talking points here.")
    current_architecture_notes = st.text_area("Key points about current architecture")

    st.subheader("3. Gap Check (Notes)")
    gap_insights = st.text_area("Key insights from updated gaps (risks, shortfalls, strengths)")

    st.markdown("---")

    # --- Step 4: Micro-Upgrade ---
    st.subheader("4. Micro-Upgrade Options")
    upgrade_option_chosen = st.radio(
        "Which option did the client lean towards?",
        ["None yet", "Must", "Should", "Could"],
        index=0
    )
    upgrade_notes = st.text_area("Notes on upgrade discussion (no pressure, just clarity)")

    st.markdown("---")

    # --- Step 5: Referrals ---
    st.subheader("5. Referrals")
    st.caption("Use the warm script: people going through life changes who could use a quick clarity scan.")
    referral_names = st.text_area("Names & relationships (if any)")
    referral_context = st.text_area("Context (what change they’re going through, how to approach, etc.)")

    st.markdown("---")

    # --- Step 6: Follow-Up ---
    st.subheader("6. Follow-Up Actions")
    follow_up_actions = st.text_area("What will you send/do after this meeting? (Blueprint, WhatsApp, call, etc.)")

    st.markdown("---")

    # --- Summary generation ---
    st.subheader("Review Summary")
    if st.button("Generate Summary"):
        data = ReviewMeetingData(
            client_id=client_id,
            client_name=client_name or client_id,
            meeting_datetime=meeting_time,
            life_changes=life_changes,
            new_goals=new_goals,
            upcoming_decisions=upcoming_decisions,
            current_architecture_notes=current_architecture_notes,
            gap_insights=gap_insights,
            upgrade_option_chosen=upgrade_option_chosen,
            upgrade_notes=upgrade_notes,
            referral_names=referral_names,
            referral_context=referral_context,
            follow_up_actions=follow_up_actions,
        )
        summary = create_review_summary(data)
        st.text_area("Copy/Paste Summary", summary, height=400)
        st.success("Summary generated. You can paste this into email, WhatsApp, or your notes system.")

if __name__ == "__main__":
    main()
