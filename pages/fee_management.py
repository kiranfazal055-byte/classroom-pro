import streamlit as st
import pandas as pd

st.header("Fee Management")

students = pd.read_csv("data/students.csv")
courses = pd.read_csv("data/courses.csv")

st.write("Fee status coming soon!")
st.dataframe(students[['id', 'name']])