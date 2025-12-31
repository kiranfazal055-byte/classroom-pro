import streamlit as st
import pandas as pd

st.header("Manage Teachers")

teachers = pd.read_csv("data/teachers.csv") if os.path.exists("data/teachers.csv") else pd.DataFrame(columns=["id", "name", "subject", "email"])

with st.expander("Add New Teacher"):
    with st.form("add_teacher"):
        name = st.text_input("Name")
        subject = st.text_input("Subject")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add")
        if submitted:
            new_id = teachers['id'].max() + 1 if not teachers.empty else 1
            new_teacher = pd.DataFrame([{"id": new_id, "name": name, "subject": subject, "email": email}])
            teachers = pd.concat([teachers, new_teacher], ignore_index=True)
            teachers.to_csv("data/teachers.csv", index=False)
            st.success("Teacher added!")
            st.rerun()

st.dataframe(teachers)