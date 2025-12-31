import streamlit as st
import pandas as pd
from datetime import date

st.header("Schedule Exam")

exams = pd.read_csv("data/exams.csv") if os.path.exists("data/exams.csv") else pd.DataFrame(columns=["id", "exam_name", "date", "subject", "class_id"])

classes = pd.read_csv("data/classes.csv")

with st.expander("Schedule New Exam"):
    with st.form("schedule_exam"):
        exam_name = st.text_input("Exam Name (e.g., Mid Term)")
        subject = st.text_input("Subject")
        exam_date = st.date_input("Exam Date", min_value=date.today())
        class_choice = st.selectbox("Class", classes['class_name'])
        class_id = classes[classes['class_name'] == class_choice]['id'].iloc[0]
        submitted = st.form_submit_button("Schedule")
        if submitted:
            new_id = exams['id'].max() + 1 if not exams.empty else 1
            new_exam = pd.DataFrame([{"id": new_id, "exam_name": exam_name, "date": str(exam_date), "subject": subject, "class_id": class_id}])
            exams = pd.concat([exams, new_exam], ignore_index=True)
            exams.to_csv("data/exams.csv", index=False)
            st.success("Exam scheduled!")
            st.rerun()

st.dataframe(exams.merge(classes, left_on='class_id', right_on='id')[['exam_name', 'subject', 'date', 'class_name']])