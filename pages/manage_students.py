import streamlit as st
import pandas as pd

st.header("Manage Students")

students = pd.read_csv("data/students.csv") if os.path.exists("data/students.csv") else pd.DataFrame(columns=["id", "name", "email", "phone", "age", "gender", "class"])

with st.expander("Add New Student"):
    with st.form("add_student"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        age = st.number_input("Age", min_value=5)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        class_name = st.text_input("Class/Section")
        submitted = st.form_submit_button("Add")
        if submitted:
            new_id = students['id'].max() + 1 if not students.empty else 1
            new_student = pd.DataFrame([{"id": new_id, "name": name, "email": email, "phone": phone, "age": age, "gender": gender, "class": class_name}])
            students = pd.concat([students, new_student], ignore_index=True)
            students.to_csv("data/students.csv", index=False)
            st.success("Student added!")
            st.rerun()

st.dataframe(students)