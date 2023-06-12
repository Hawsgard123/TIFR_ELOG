# Library call
import psycopg2
import streamlit as st
import datetime
import pandas as pd

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="test",
    user="postgres",
    password="hawsgard@12345",
)

cur = conn.cursor()

# Config
st.set_page_config(
    page_title="ELOG TIFR",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Headers
st.header("TIFR Pelletron - Linac Facility ELOG")
st.subheader("Operator Directory")
"---"

# Body
name = st.text_input("Operator Name")
opID = st.text_input("Operator ID")
op_details = st.text_area("Operation Details")

col1, col2 = st.columns([1, 1])
with col1:
    date = st.date_input("Enter today's date")
with col2:
    time = st.time_input("Enter time")

type = st.selectbox(
    "Choose Operation Type", ("Manual Entry", "Repair Work", "Routine Check", "Other")
)

if type == "Other":
    st.text_input("Enter the type")

# Create a button with a label of "Submit"
submit_button = st.button("Submit")

if submit_button:
    st.write("Your data has been saved.")

    cur = conn.cursor()
    cur.execute(
        """insert into operator (opID, name, op_details, date, time, type) values (%s, %s, %s, %s, %s, %s)""",
        (opID, name, op_details, date, time, type),
    )
    conn.commit()

df = pd.read_sql("select * from operator", conn)
st.table(df)
