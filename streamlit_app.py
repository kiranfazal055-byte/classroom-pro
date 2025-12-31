import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import calendar
import os

st.set_page_config(page_title="School Pro", page_icon="🏫", layout="wide")

# Safe load data
def load_data(file):
    path = f"data/{file}"
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        columns = {
            "students.csv": ["id", "name", "email", "class"],
            "teachers.csv": ["id", "name", "subject"],
            "classes.csv": ["id", "name"],
            "quiz_questions.csv": ["question", "opt1", "opt2", "opt3", "opt4", "correct"],
            "quiz_results.csv": ["student_id", "score", "total", "percentage", "date"]
        }
        return pd.DataFrame(columns=columns.get(file, []))
    return pd.read_csv(path)

students = load_data("students.csv")
teachers = load_data("teachers.csv")
classes = load_data("classes.csv")
quiz_questions = load_data("quiz_questions.csv")
quiz_results = load_data("quiz_results.csv")

# Fake events for calendar
events = [
    {"day": 10, "title": "Graduation Ceremony", "color": "#10b981"},
    {"day": 12, "title": "Parents Meeting", "color": "#ef4444"},
]

# Login Screen
if "role" not in st.session_state:
    st.title("🏫 Welcome to School Pro")
    role = st.radio("Login as", ("Admin", "Student"))
    if role == "Admin":
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if password == "admin123":
                st.session_state.role = "admin"
                st.rerun()
            else:
                st.error("Wrong password")
    else:
        student_id = st.text_input("Your Student ID")
        if st.button("Login"):
            if student_id in students['id'].astype(str).values:
                st.session_state.role = "student"
                st.session_state.student_id = student_id
                st.rerun()
            else:
                st.error("Invalid ID")

# Admin Dashboard
elif st.session_state.role == "admin":
    with st.sidebar:
        st.image("https://via.placeholder.com/150?text=School+Logo", width=150)  # Replace with real logo
        st.title("School Pro")
        choice = st.radio("Navigate", [
            "Dashboard", "Students", "Teachers", "Classes", "Create Quiz", "Attendance", "Fees", "Report Cards"
        ])
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    if choice == "Dashboard":
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://randomuser.me/api/portraits/men/1.jpg", width=150)
            st.markdown("### Welcome, Admin!")
            st.metric("Students", len(students))
            st.metric("Classes", len(classes))
            st.metric("Teachers", len(teachers))

            st.markdown("#### Quick Actions")
            st.button("➕ Add Student")
            st.button("📊 View Attendance")
            st.button("📧 Messages")

            st.markdown("#### Announcements")
            st.info("National Day Holiday")
            st.info("Parent Meeting - Feb 12")

        with col2:
            st.markdown("### 📅 Calendar - February 2026")
            cal = calendar.monthcalendar(2026, 2)
            html = "<table style='width:100%;border-collapse:collapse;'>"
            for week in cal:
                html += "<tr>"
                for day in week:
                    color = "white"
                    title = ""
                    for e in events:
                        if day == e["day"]:
                            color = e["color"]
                            title = e["title"]
                    if day == 0:
                        html += "<td></td>"
                    else:
                        html += f"<td style='border:1px solid #ddd;padding:20px;background:{color};color:white;text-align:center;'>{day}<br><small>{title}</small></td>"
                html += "</tr>"
            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)

        st.markdown("### 📈 Analytics")
        col1, col2 = st.columns(2)
        df_att = pd.DataFrame({"Month": ["Jan", "Feb", "Mar"], "Attendance %": [95, 92, 98]})
        fig = px.line(df_att, x="Month", y="Attendance %", title="Attendance Trend")
        col1.plotly_chart(fig, use_container_width=True)

        df_gender = pd.DataFrame({"Gender": ["Male", "Female"], "Count": [220, 190]})
        fig_pie = px.pie(df_gender, names="Gender", values="Count", title="Students by Gender")
        col2.plotly_chart(fig_pie, use_container_width=True)

    else:
        st.switch_page(f"pages/{choice.lower().replace(' ', '_')}.py")

# Student Portal
else:
    st.switch_page("pages/student_portal.py")S