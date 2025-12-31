import streamlit as st
import pandas as pd
import os

st.title("📊 Report Cards")

results_path = "data/quiz_results.csv"
if not os.path.exists(results_path):
    st.info("No results yet.")
else:
    results = pd.read_csv(results_path)
    students = pd.read_csv("data/students.csv")
    merged = results.merge(students, left_on="student_id", right_on="id")

    for _, row in merged.iterrows():
        with st.expander(f"{row['name']} - {row['score']}/{row['total']} ({row['percentage']:.1f}%)"):
            st.write(f"**Date:** {row['date']}")
            grade = "A" if row['percentage'] >= 90 else "B" if row['percentage'] >= 80 else "C"
            st.write(f"**Grade:** {grade}")