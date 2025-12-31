import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

st.title("📅 Schedule Exam")

# Load classes and exams
classes = pd.read_csv("data/classes.csv") if os.path.exists("data/classes.csv") else pd.DataFrame(columns=["id", "name"])
path = "data/exams.csv"
exams = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=["id", "exam_name", "date", "time", "subject", "class_id"])

if classes.empty:
    st.warning("Please add classes first in 'Classes' section.")
else:
    with st.form("schedule_exam"):
        st.subheader("Schedule New Exam")
        exam_name = st.text_input("Exam Name (e.g., Mid-Term Math)")
        subject = st.text_input("Subject")
        class_id = st.selectbox(
            "Select Class",
            classes['id'],
            format_func=lambda x: classes[classes['id'] == x]['name'].iloc[0]
        )
        col1, col2 = st.columns(2)
        exam_date = col1.date_input("Exam Date", date.today())
        exam_time = col2.time_input("Exam Time", datetime.strptime("10:00", "%H:%M").time())

        if st.form_submit_button("Schedule Exam"):
            new_id = exams['id'].max() + 1 if not exams.empty else 1
            new_exam = pd.DataFrame([{
                "id": new_id,
                "exam_name": exam_name,
                "date": str(exam_date),
                "time": str(exam_time),
                "subject": subject,
                "class_id": class_id
            }])
            exams = pd.concat([exams, new_exam], ignore_index=True)
            exams.to_csv(path, index=False)
            st.success(f"Exam '{exam_name}' scheduled successfully!")
            st.balloons()
            st.rerun()

    st.subheader("Scheduled Exams")
    if not exams.empty:
        # Merge with class names for display
        display_exams = exams.merge(classes, left_on="class_id", right_on="id", how="left")
        display_exams = display_exams.rename(columns={"name": "class_name"})
        display_exams = display_exams[["exam_name", "subject", "class_name", "date", "time"]]
        st.dataframe(display_exams, use_container_width=True)

        # Delete exam
        exam_id = st.selectbox("Select Exam to Delete", exams['id'])
        if st.button("Delete Exam", type="primary"):
            exams = exams[exams['id'] != exam_id]
            exams.to_csv(path, index=False)
            st.success("Exam deleted!")
            st.rerun()
    else:
        st.info("No exams scheduled yet.")