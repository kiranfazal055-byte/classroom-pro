import streamlit as st
import pandas as pd
from datetime import date

st.header("Attendance Management")

students = pd.read_csv("data/students.csv")
today = date.today().strftime("%Y-%m-%d")

with st.form("attendance_form"):
    st.write(f"Mark Attendance for {today}")
    attendance_dict = {}
    for _, student in students.iterrows():
        attendance_dict[student['name']] = st.checkbox(student['name'], value=True)

    submitted = st.form_submit_button("Save Attendance")
    if submitted:
        records = []
        for name, present in attendance_dict.items():
            student_id = students[students['name'] == name]['id'].iloc[0]
            records.append({"student_id": student_id, "date": today, "present": 1 if present else 0})
        new_att = pd.DataFrame(records)
        new_att.to_csv("data/attendance.csv", mode='a', header=not os.path.exists("data/attendance.csv"), index=False)
        st.success("Attendance saved!")

st.dataframe(pd.read_csv("data/attendance.csv"))