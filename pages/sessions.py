import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("📚 Session Management")

path = "data/sessions.csv"
sessions = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=["id", "session_name", "start_date", "end_date", "current"])

with st.form("add_session"):
    st.subheader("Add New Academic Session")
    session_name = st.text_input("Session Name (e.g., 2025-2026)")
    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date", datetime(2025, 9, 1))
    end_date = col2.date_input("End Date", datetime(2026, 6, 30))
    current = st.checkbox("Mark as Current Session")

    if st.form_submit_button("Add Session"):
        new_id = sessions['id'].max() + 1 if not sessions.empty else 1
        new_row = pd.DataFrame([{
            "id": new_id,
            "session_name": session_name,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "current": current
        }])
        sessions = pd.concat([sessions, new_row], ignore_index=True)
        sessions.to_csv(path, index=False)
        st.success("Session added!")
        st.rerun()

st.subheader("Current Sessions")
if not sessions.empty:
    st.dataframe(sessions)
    current_session = sessions[sessions['current'] == True]
    if not current_session.empty:
        st.success(f"Current Session: {current_session.iloc[0]['session_name']}")
else:
    st.info("No sessions added yet.")