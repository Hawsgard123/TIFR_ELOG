import streamlit as st
import pandas as pd
import psycopg2

# Initialize connection.
conn = psycopg2.connect(
    host='localhost',
    port='5432',
    database='tifrmock',
    user='postgres',
    password='asdf@123',
)

st.set_page_config(
    page_title="ELOG TIFR RETRIVE 01",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.header("Search ELOGS")

# Create a form to get the data to search for.
search_name = st.sidebar.text_input("Enter the Operator Name to search for:")
search_opID = st.sidebar.text_input("Enter the Operator ID to search for:")
search_type = st.sidebar.text_input("Enter the Type to search for:")

col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.sidebar.date_input("Enter the Start Date to search for:")
with col2:
    end_date = st.sidebar.date_input("Enter the End Date to search for:")

st.header("Saved Linac Facility ELOG")
"---"

query = f"SELECT id, name, opID, op_details, date, time, type FROM tifrop ORDER BY id DESC LIMIT 5;"
with conn.cursor() as cur:
    cur.execute(query)
    rows = cur.fetchall()  

if rows:
    for row in rows:
        df = pd.DataFrame(rows, columns=['id', 'name', 'opID', 'operator details', 'date', 'time', 'type'])
    st.table(df)

"---"
# If the user enters some name, search the database for it.
if search_name:
    query = f"SELECT id, name, opID, date, time, type FROM tifrop WHERE name = '{search_name}';"
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()  

    # If there are any results, display them.
    if rows:
        for row in rows:
            df = pd.DataFrame(rows, columns=['id', 'name', 'opID', 'date', 'time', 'type'])
        st.table(df)

# If the user enters some opID, search the database for it.
elif search_opID:
    query = f"SELECT id, name, opID, date, time, type FROM tifrop WHERE opID = '{search_opID}';"
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()  

    # If there are any results, display them.
    if rows:
        for row in rows:
            df = pd.DataFrame(rows, columns=['id', 'name', 'opID', 'date', 'time', 'type'])
        st.table(df)

# If the user enters some opID, search the database for it.
elif search_type:
    query = f"SELECT id, name, opID, date, time, type FROM tifrop WHERE opID = '{search_opID}';"
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()  

    # If there are any results, display them.
    if rows:
        for row in rows:
            df = pd.DataFrame(rows, columns=['id', 'name', 'opID', 'date', 'time', 'type'])
        st.table(df)

# If the user enters some date range, search the database for it.
elif start_date:
    if end_date:
        query = f"SELECT id, name, opID, date, time, type FROM tifrop WHERE date between '{start_date}' AND '{end_date}';"
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()  

    # If there are any results, display them.
    if rows:
        for row in rows:
            df = pd.DataFrame(rows, columns=['id', 'name', 'opID', 'date', 'time', 'type'])
        st.table(df)


st.sidebar.write("----")

delete_id = st.sidebar.text_input("Enter the ID of the tuple to be deleted (if any)")

delete_button = st.sidebar.button("DELETE")

#If the delete button is pressed
if delete_button:
    
    #delete_id = st.sidebar.text_input("Enter the ID of the tuple to be deleted (if any)")

    #delete_confirm = st.sidebar.button("CONFIRM DELETION")
    #if delete_confirm:
    
    query = f"DELETE FROM tifrop WHERE id = {delete_id};"

    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()  
        
# Close the connection to the database.
conn.close()        

