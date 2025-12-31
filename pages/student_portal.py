import streamlit as st
import pandas as pd
from datetime import datetime

st.title(f"Welcome, {st.session_state.student_name} 👋")

students = pd.read_csv("data/students.csv")
quiz_questions = pd.read_csv("data/quiz_questions.csv")

my_data = students[students['id'] == int(st.session_state.student_id)].iloc[0]

st.subheader("Your Profile")
st.write(f"**ID:** {my_data['id']}")
st.write(f"**Name:** {my_data['name']}")
st.write(f"**Email:** {my_data['email']}")
st.write(f"**Class:** {my_data.get('class', 'N/A')}")

st.subheader("Take Quiz")
if quiz_questions.empty:
    st.info("No quiz available yet.")
else:
    with st.form("quiz_form"):
        score = 0
        total = len(quiz_questions)
        for i, row in quiz_questions.iterrows():
            answer = st.radio(row['question'], [row['opt1'], row['opt2'], row['opt3'], row['opt4']], key=f"q{i}")
            if answer == row['correct']:
                score += 1

        submitted = st.form_submit_button("Submit Quiz")
        if submitted:
            percentage = (score / total) * 100
            st.success(f"You scored {score}/{total} ({percentage:.1f}%)")

            # Grade & Comment
            if percentage >= 90:
                grade = "A"
                comment = "Excellent performance! 🌟 Keep it up!"
            elif percentage >= 80:
                grade = "B"
                comment = "Great job! You're doing really well! 👍"
            elif percentage >= 70:
                grade = "C"
                comment = "Good effort! You can do even better! 💪"
            elif percentage >= 60:
                grade = "D"
                comment = "Needs improvement. Practice more! 📚"
            else:
                grade = "F"
                comment = "Don't worry — keep trying! We believe in you!"

            st.write(f"**Grade:** {grade}")
            st.write(f"**Teacher Comment:** {comment}")

            if percentage >= 80:
                st.balloons()

            # === REPORT CARD ===
            st.subheader("Your Report Card")
            st.markdown("---")

            # Student info
            st.write(f"**Student Name:** {st.session_state.student_name}")
            st.write(f"**Student ID:** {st.session_state.student_id}")
            st.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

            # Quiz result
            st.write(f"**Quiz Score:** {score}/{total}")
            st.write(f"**Percentage:** {percentage:.1f}%")
            st.write(f"**Grade:** {grade}")
            st.write(f"**Comment:** {comment}")

            # Download as HTML (open in browser → print as PDF)
            report_html = f"""
            <h1>Report Card</h1>
            <p><strong>Student Name:</strong> {st.session_state.student_name}</p>
            <p><strong>Student ID:</strong> {st.session_state.student_id}</p>
            <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <p><strong>Quiz Score:</strong> {score}/{total} ({percentage:.1f}%)</p>
            <p><strong>Grade:</strong> {grade}</p>
            <p><strong>Teacher Comment:</strong> {comment}</p>
            """
            st.download_button(
                label="📄 Download Report Card (HTML/PDF)",
                data=report_html,
                file_name=f"report_card_{st.session_state.student_id}_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )