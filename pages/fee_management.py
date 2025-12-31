import streamlit as st
import pandas as pd
import os

st.title("💰 Fee Management")

students = pd.read_csv("data/students.csv") if os.path.exists("data/students.csv") else pd.DataFrame()
path = "data/fees.csv"
fees = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=["student_id", "amount_due", "amount_paid", "balance", "last_payment"])

if students.empty:
    st.warning("No students added yet.")
else:
    student_id = st.selectbox("Select Student", students['id'], format_func=lambda x: students[students['id'] == x]['name'].iloc[0])

    student_fees = fees[fees['student_id'] == student_id]
    if student_fees.empty:
        # Create new fee record
        amount_due = st.number_input("Total Fee Amount", min_value=0.0, value=5000.0)
        amount_paid = st.number_input("Amount Paid", min_value=0.0, value=0.0)
        balance = amount_due - amount_paid
        if st.button("Save Fee Record"):
            new_fee = pd.DataFrame([{
                "student_id": student_id,
                "amount_due": amount_due,
                "amount_paid": amount_paid,
                "balance": balance,
                "last_payment": date.today().strftime("%Y-%m-%d")
            }])
            fees = pd.concat([fees, new_fee], ignore_index=True)
            fees.to_csv(path, index=False)
            st.success("Fee record created!")
    else:
        fee = student_fees.iloc[0]
        st.write(f"**Total Due:** ${fee['amount_due']}")
        st.write(f"**Paid:** ${fee['amount_paid']}")
        st.write(f"**Balance:** ${fee['balance']}")

        payment = st.number_input("Record Payment", min_value=0.0)
        if st.button("Record Payment"):
            new_paid = fee['amount_paid'] + payment
            new_balance = fee['amount_due'] - new_paid
            fees.loc[fees['student_id'] == student_id, ['amount_paid', 'balance', 'last_payment']] = [new_paid, new_balance, date.today().strftime("%Y-%m-%d")]
            fees.to_csv(path, index=False)
            st.success("Payment recorded!")
            st.rerun()

    st.subheader("All Fee Records")
    if not fees.empty:
        merged = fees.merge(students, left_on="student_id", right_on="id")
        st.dataframe(merged[["name", "amount_due", "amount_paid", "balance"]])