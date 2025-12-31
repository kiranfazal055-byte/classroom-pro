import streamlit as st
import pandas as pd
import os

st.title("🏫 Manage Classes")

path = "data/classes.csv"
classes = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=["id", "name"])

with st.form("add_class"):
    class_name = st.text_input("Class Name (e.g., Grade 10A)")
    if st.form_submit_button("Add Class"):
        new_id = classes['id'].max() + 1 if not classes.empty else 1
        new_row = pd.DataFrame([{"id": new_id, "name": class_name}])
        classes = pd.concat([classes, new_row], ignore_index=True)
        classes.to_csv(path, index=False)
        st.success("Class added!")
        st.rerun()

st.dataframe(classes)