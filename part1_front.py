# Library call
import psycopg2
import streamlit as st
import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import tempfile
import os

# Config
st.set_page_config(
    page_title="ELOG TIFR", layout="wide", initial_sidebar_state="expanded"
)

# Path to the txt file containing the descriptions and column headers
txt_file_path = "data.txt"

# Add template code
string = st.sidebar.text_input("Enter the template")
st.sidebar.caption(
    "Format: 'The name of the template', 'Column name 1', 'Column name 2', ..."
)
but = st.sidebar.button("Add this template")
if but:
    with open(txt_file_path, "a") as f:
        f.write(string + "\n")
    st.sidebar.success("Added Successfully")
    f.close()

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="test",
    user="postgres",
    password="hawsgard@12345",
)

cur = conn.cursor()
# Headers
st.header("TIFR Pelletron - Linac Facility ELOG")
st.subheader("Operator Directory")

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
    type = st.text_input("Enter the type")


# traverse through the headers
def find_column_headers(txt_file_path, option):
    if option == "Empty sheet":
        return ""
    with open(txt_file_path, "r") as file:
        lines = file.readlines()

    column_headers = []
    for line in lines:
        if option in line:
            column_headers = line.strip().split(",")[1:]
            break

    file.close()
    return column_headers


# create the file
def create_excel_file(column_headers):
    workbook = Workbook()
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    sheet = workbook.active
    df = pd.DataFrame(columns=column_headers)

    for row in dataframe_to_rows(df, index=False, header=True):
        sheet.append(row)
    file_path = temp_file.name
    workbook.save(file_path)

    return file_path


# save the file
def save_excel_file(file, save_location):
    with open(save_location, "wb") as f:
        f.write(file.getbuffer())

    return save_location


with st.expander("Sheets for Observation table"):
    # Read descriptions from the txt file

    with open(txt_file_path, "r") as file:
        descriptions = [line.strip().split(",")[0] for line in file.readlines()]
    selected_option = st.selectbox("Select an option", descriptions)

    # Find column headers for the selected option and display the line number
    column_headers = find_column_headers(txt_file_path, selected_option)

    # Create an Excel file with the column headers
    st.download_button(
        label="Download",
        data=open(create_excel_file(column_headers), "rb").read(),
        file_name="empty_excel_sheet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

anomaly = st.text_area("Any anomaly found? Note it down")

if anomaly == None:
    anomaly = "No Issues"

uploaded_file = st.file_uploader("Upload excel file")

file_name = uploaded_file.name
save_location = f"obs_table/{file_name}"

loc = save_excel_file(uploaded_file, save_location)


# Create a button with a label of "Submit"
submit_button = st.button("Submit")

if submit_button:
    st.write("Your data has been saved.")

    cur = conn.cursor()
    cur.execute(
        """insert into operator (date, time, name, opID, op_details, type, anomaly, loc) values (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (date, time, name, opID, op_details, type, anomaly, loc),
    )
    conn.commit()
