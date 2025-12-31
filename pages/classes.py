import streamlit as st
import pandas as pd

st.header("Manage Classes")

classes = pd.read_csv("data/classes.csv") if os.path.exists("data/classes.csv") else pd.DataFrame(columns=["id", "class_name", "grade_level"])

with st.expander("Add New Class"):
    with st.form("add_class"):
        class_name = st.text_input("Class Name (e.g., Class 10A)")
        grade_level = st.selectbox("Grade Level", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
        submitted = st.form_submit_button("Add Class")
        if submitted:
            new_id = classes['id'].max() + 1 if not classes.empty else 1
            new_class = pd.DataFrame([{"id": new_id, "class_name": class_name, "grade_level": grade_level}])
            classes = pd.concat([classes, new_class], ignore_index=True)
            classes.to_csv("data/classes.csv", index=False)
            st.success("Class added!")
            st.rerun()

st.dataframe(classes)