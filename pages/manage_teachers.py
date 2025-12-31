import streamlit as st
import pandas as pd
import os

st.title("👩‍🏫 Manage Teachers")

path = "data/teachers.csv"
teachers = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=["id", "name", "subject"])

with st.form("add_teacher"):
    name = st.text_input("Teacher Name")
    subject = st.text_input("Subject")
    if st.form_submit_button("Add Teacher"):
        new_id = teachers['id'].max() + 1 if not teachers.empty else 1
        new_row = pd.DataFrame([{"id": new_id, "name": name, "subject": subject}])
        teachers = pd.concat([teachers, new_row], ignore_index=True)
        teachers.to_csv(path, index=False)
        st.success("Teacher added!")
        st.rerun()

st.dataframe(teachers)