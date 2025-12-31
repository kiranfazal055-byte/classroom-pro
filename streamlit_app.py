import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title="Classroom Management", page_icon="🏫", layout="wide")

# Safe load data
def load_data(file):
    path = f"data/{file}"
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        columns = {
            "students.csv": ["id", "name", "email", "phone", "age", "gender", "class"],
            "teachers.csv": ["id", "name", "subject", "email"],
            "classes.csv": ["id", "class_name", "grade_level"],
            "sections.csv": ["id", "class_id", "section_name"],
            "exams.csv": ["id", "exam_name", "date", "subject", "class_id"],
            "sessions.csv": ["id", "session_name", "start_date", "end_date", "current"],
            "quiz_questions.csv": ["question", "opt1", "opt2", "opt3", "opt4", "correct"],
            "attendance.csv": ["student_id", "date", "present"],
            "report_card.csv": ["student_id", "score", "total", "percentage", "date"]  # if you have this
        }
        return pd.DataFrame(columns=columns.get(file, []))
    else:
        return pd.read_csv(path)

# Load data
students = load_data("students.csv")
teachers = load_data("teachers.csv")
classes = load_data("classes.csv")
sections = load_data("sections.csv")
exams = load_data("exams.csv")
sessions = load_data("sessions.csv")
quiz_questions = load_data("quiz_questions.csv")
attendance = load_data("attendance.csv")

# Title
st.title("🏫 Classroom Pro")

# Login
role = st.radio("Login as", ("Admin", "Student"))

if role == "Admin":
    password = st.text_input("Admin Password", type="password")
    if st.button("Login as Admin"):
        if password == "admin123":  # Change this password!
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.success("Admin logged in successfully!")
            st.rerun()
        else:
            st.error("Incorrect password")

elif role == "Student":
    student_id = st.text_input("Enter your Student ID")
    if st.button("Login as Student"):
        if not students.empty and student_id in students['id'].astype(str).values:
            st.session_state.logged_in = True
            st.session_state.role = "student"
            st.session_state.student_id = student_id
            st.session_state.student_name = students[students['id'] == int(student_id)]['name'].iloc[0]
            st.success(f"Welcome back, {st.session_state.student_name}!")
            st.rerun()
        else:
            st.error("Invalid Student ID")

# Logout
if st.session_state.get("logged_in"):
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

# Admin Navigation
if st.session_state.get("role") == "admin":
    st.sidebar.title("Admin Navigation")
    choice = st.sidebar.radio("Navigate", [
        "Dashboard",
        "Manage Students",
        "Manage Teachers",
        "Classes",
        "Sections",
        "Schedule Exam",
        "Session Management",
        "Create Quiz",
        "Attendance",
        "Fees",
        "Report Cards"
    ])

    if choice == "Dashboard":
        st.header("📊 Admin Dashboard")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Students", len(students))
        col2.metric("Total Teachers", len(teachers))
        col3.metric("Total Classes", len(classes))
        col4.metric("Total Exams", len(exams))

        if not students.empty:
            fig = px.pie(students, names="gender", title="Gender Distribution")
            st.plotly_chart(fig, use_container_width=True)

    elif choice == "Manage Students":
        st.switch_page("pages/manage_students.py")
    elif choice == "Manage Teachers":
        st.switch_page("pages/manage_teachers.py")
    elif choice == "Classes":
        st.switch_page("pages/classes.py")
    elif choice == "Sections":
        st.switch_page("pages/sections.py")
    elif choice == "Schedule Exam":
        st.switch_page("pages/schedule_exam.py")
    elif choice == "Session Management":
        st.switch_page("pages/sessions.py")
    elif choice == "Create Quiz":
        st.switch_page("pages/create_quiz.py")
    elif choice == "Attendance":
        st.switch_page("pages/attendance.py")
    elif choice == "Fees":
        st.switch_page("pages/fee_management.py")
    elif choice == "Report Cards":
        st.switch_page("pages/report_cards.py")

# Student Portal
if st.session_state.get("role") == "student":
    st.switch_page("pages/student_portal.py")

st.caption("Classroom Pro • Professional School Management • 2025")
