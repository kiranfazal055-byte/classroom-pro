import streamlit as st
import pandas as pd

st.header("Academic Session Management")

sessions = pd.read_csv("data/sessions.csv") if os.path.exists("data/sessions.csv") else pd.DataFrame(columns=["id", "session_name", "start_date", "end_date", "current"])

with st.expander("Add New Session"):
    with st.form("add_session"):
        session_name = st.text_input("Session Name (e.g., 2025-2026)")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        current = st.checkbox("Mark as Current Session")
        submitted = st.form_submit_button("Add Session")
        if submitted:
            if current:
                sessions['current'] = False  # Only one current
            new_id = sessions['id'].max() + 1 if not sessions.empty else 1
            new_session = pd.DataFrame([{"id": new_id, "session_name": session_name, "start_date": str(start_date), "end_date": str(end_date), "current": current}])
            sessions = pd.concat([sessions, new_session], ignore_index=True)
            sessions.to_csv("data/sessions.csv", index=False)
            st.success("Session added!")
            st.rerun()

st.dataframe(sessions)