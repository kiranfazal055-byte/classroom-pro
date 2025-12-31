import streamlit as st
import pandas as pd

st.header("Manage Sections")

classes = pd.read_csv("data/classes.csv")
sections = pd.read_csv("data/sections.csv") if os.path.exists("data/sections.csv") else pd.DataFrame(columns=["id", "class_id", "section_name", "teacher_id"])

with st.expander("Add New Section"):
    with st.form("add_section"):
        class_choice = st.selectbox("Select Class", classes['class_name'])
        class_id = classes[classes['class_name'] == class_choice]['id'].iloc[0]
        section_name = st.text_input("Section Name (e.g., A, B, Science)")
        submitted = st.form_submit_button("Add Section")
        if submitted:
            new_id = sections['id'].max() + 1 if not sections.empty else 1
            new_section = pd.DataFrame([{"id": new_id, "class_id": class_id, "section_name": section_name}])
            sections = pd.concat([sections, new_section], ignore_index=True)
            sections.to_csv("data/sections.csv", index=False)
            st.success("Section added!")
            st.rerun()

# Show sections with class name
if not sections.empty and not classes.empty:
    merged = sections.merge(classes, left_on='class_id', right_on='id', suffixes=('', '_class'))
    st.dataframe(merged[['class_name', 'section_name']])