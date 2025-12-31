import streamlit as st
import pandas as pd
from datetime import date
import os

st.title("📅 Attendance Management")

students = pd.read_csv("data/students.csv") if os.path.exists("data/students.csv") else pd.DataFrame()
path = "data/attendance.csv"
attendance = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=["student_id", "date", "present"])

today = date.today().strftime("%Y-%m-%d")

if students.empty:
    st.warning("No students added yet.")
else:
    st.subheader(f"Mark Attendance - {today}")
    with st.form("attendance_form"):
        attendance_dict = {}
        for _, student in students.iterrows():
            attendance_dict[student['id']] = st.checkbox(f"{student['name']} ({student['class']})", key=student['id'])

        submitted = st.form_submit_button("Save Attendance")
        if submitted:
            records = []
            for sid, present in attendance_dict.items():
                records.append({"student_id": sid, "date": today, "present": present})
            new_att = pd.DataFrame(records)
            attendance = pd.concat([attendance, new_att], ignore_index=True)
            attendance.to_csv(path, index=False)
            st.success("Attendance saved for today!")
            st.balloons()

    st.subheader("Attendance Records")
    if not attendance.empty:
        st.dataframe(attendance.merge(students, left_on="student_id", right_on="id")[["name", "date", "present"]])
    else:
        st.info("No attendance records yet.")