# Library call
import psycopg2
import streamlit as st
import datetime
import pandas as pd
import os
import webbrowser


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
        f.write("\n" + string)
    st.sidebar.success("Added Successfully")
    f.close()

with open(txt_file_path, "r") as file:
    descriptions = [line.strip().split(",")[0] for line in file.readlines()]
selected_option = st.sidebar.selectbox("Select an option", descriptions)

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

def find_column_headers(option):
    with open(txt_file_path, "r") as f:
        lines = f.readlines()
    
    column_readers = []
    for line in lines:
        if option in line:
            column_headers = line.strip().split(",")[1:]
            break
    
    f.close()
    return column_headers

save_folder = f"obs_table/{name}/{date}"

table_name = st.text_input("Enter a name for the table")
st.caption("Use a different name for the table, same or used names might replace the previous table with new data.")
column_headers = find_column_headers(selected_option)
df = pd.DataFrame(columns = column_headers)
table = st.data_editor(df, num_rows = "dynamic", use_container_width=True)

if st.button("save"):
    os.makedirs(save_folder, exist_ok=True)
    table.to_excel(f"{save_folder}/{table_name}.xlsx", index=True)
    loc = f"{sav_folder}/{table_name}.xlsx"
    st.success("Table saved successfully")

anomaly = st.text_area("Fill the box if any anomaly")

if anomaly == None:
    anomaly = "No Issues"


if st.button("Submit"):
    st.write("Your data has been saved.")

    cur = conn.cursor()
    cur.execute(
        """insert into operator (date, time, name, opID, op_details, type, anomaly, loc) values (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (date, time, name, opID, op_details, type, anomaly, loc),
    )
    conn.commit()





#First about TIFR
#Then about Pelletron

#scope of your work - requirement and solution - screenshot of page
#technology used
#scope for future
#learning

#accelertor and its control system 
#project requirement in the facility
#github upload

#user manual in easiest way possible 
#how to use and its solutions 
#troubleshooting and fixing 
