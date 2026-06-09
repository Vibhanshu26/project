import streamlit as st
import sqlite3
from datetime import datetime

# Create/connect database
conn = sqlite3.connect("registration.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    dob TEXT,
    designation TEXT
)
""")
conn.commit()

st.set_page_config(layout="wide")

with st.form("myform"):
    st.subheader("Registration Form")

    c1, c2, c3 = st.columns(3)

    title = c1.selectbox("", ("Mr", "Mrs", "Miss"))
    first_name = c2.text_input("First Name")
    last_name = c3.text_input("Last Name")

    role = st.selectbox(
        "Designation",
        ("Software", "Sr. Software", "Technical Lead",
         "Manager", "Sr. Manager", "Project Manager")
    )

    dob = st.date_input(
        "Date of Birth",
        min_value=datetime(1900, 1, 1)
    )

    gender = st.radio(
        "Select Gender",
        ("Male", "Female", "Prefer Not to Say")
    )

    age = st.slider(
        "Age",
        min_value=1,
        max_value=100,
        value=20
    )

    submitted = st.form_submit_button("Submit")

    if submitted:
        full_name = f"{title} {first_name} {last_name}"

        cursor.execute("""
        INSERT INTO registrations
        (name, age, gender, dob, designation)
        VALUES (?, ?, ?, ?, ?)
        """, (
            full_name,
            age,
            gender,
            str(dob),
            role
        ))

        conn.commit()

        st.success("Form Submitted Successfully!")

        st.json({
            "Name": full_name,
            "Age": age,
            "Gender": gender,
            "Date of Birth": dob,
            "Designation": role
        })


import pandas as pd

df = pd.read_sql_query(
    "SELECT * FROM registrations",
    conn
)

st.subheader("Registered Users")
st.dataframe(df)
