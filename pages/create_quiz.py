import streamlit as st
import pandas as pd
import os

st.title("📝 Create Quiz")

path = "data/quiz_questions.csv"
questions = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=["question", "opt1", "opt2", "opt3", "opt4", "correct"])

with st.form("add_question"):
    question = st.text_area("Question")
    col1, col2 = st.columns(2)
    opt1 = col1.text_input("Option 1")
    opt2 = col2.text_input("Option 2")
    col3, col4 = st.columns(2)
    opt3 = col3.text_input("Option 3")
    opt4 = col4.text_input("Option 4")
    correct = st.selectbox("Correct Answer", [opt1, opt2, opt3, opt4])

    if st.form_submit_button("Add Question"):
        new_row = pd.DataFrame([{
            "question": question, "opt1": opt1, "opt2": opt2, "opt3": opt3, "opt4": opt4, "correct": correct
        }])
        questions = pd.concat([questions, new_row], ignore_index=True)
        questions.to_csv(path, index=False)
        st.success("Question added!")
        st.rerun()

st.subheader("Current Questions")
st.dataframe(questions)