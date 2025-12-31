import streamlit as st
import pandas as pd

st.header("Create Quiz Questions")

questions = pd.read_csv("data/quiz_questions.csv") if os.path.exists("data/quiz_questions.csv") else pd.DataFrame(columns=["question", "opt1", "opt2", "opt3", "opt4", "correct"])

with st.form("add_question"):
    question = st.text_area("Question")
    opt1 = st.text_input("Option 1")
    opt2 = st.text_input("Option 2")
    opt3 = st.text_input("Option 3")
    opt4 = st.text_input("Option 4")
    correct = st.selectbox("Correct Answer", [opt1, opt2, opt3, opt4])
    submitted = st.form_submit_button("Add Question")
    if submitted:
        new_q = pd.DataFrame([{"question": question, "opt1": opt1, "opt2": opt2, "opt3": opt3, "opt4": opt4, "correct": correct}])
        questions = pd.concat([questions, new_q], ignore_index=True)
        questions.to_csv("data/quiz_questions.csv", index=False)
        st.success("Question added!")
        st.rerun()

st.dataframe(questions)