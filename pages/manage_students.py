import streamlit as st
import pandas as pd

st.title("👥 Manage Students")

students = pd.read_csv("data/students.csv") if os.path.exists("data/students.csv") else pd.DataFrame(columns=["id", "name", "email", "class"])

with st.form("add_student"):
    st.subheader("Add New Student")
    name = st.text_input("Name")
    email = st.text_input("Email")
    student_class = st.text_input("Class")
    if st.form_submit_button("Add Student"):
        new_id = students['id'].max() + 1 if not students.empty else 1
        new_student = pd.DataFrame([{"id": new_id, "name": name, "email": email, "class": student_class}])
        students = pd.concat([students, new_student], ignore_index=True)
        students.to_csv("data/students.csv", index=False)
        st.success("Student added!")
        st.rerun()

st.subheader("All Students")
st.dataframe(students)

if not students.empty:
    student_id = st.selectbox("Select Student to Edit/Delete", students['id'])
    student = students[students['id'] == student_id].iloc[0]
    with st.expander("Edit Student"):
        new_name = st.text_input("Name", value=student['name'])
        new_email = st.text_input("Email", value=student['email'])
        new_class = st.text_input("Class", value=student['class'])
        col1, col2 = st.columns(2)
        if col1.button("Update"):
            students.loc[students['id'] == student_id, :] = [student_id, new_name, new_email, new_class]
            students.to_csv("data/students.csv", index=False)
            st.success("Updated!")
            st.rerun()
        if col2.button("Delete", type="primary"):
            students = students[students['id'] != student_id]
            students.to_csv("data/students.csv", index=False)
            st.success("Deleted!")
            st.rerun()