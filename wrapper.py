import streamlit as st
import pandas as pd
import psycopg2
import datetime
import os
import webbrowser

st.set_page_config(
    page_title="ELOG TIFR", layout="wide", initial_sidebar_state="expanded"
)


col1, col2 = st.tabs(["E", "S"])

with col1:
        with open("part2.py") as f:
            exec(f.read())
with col2:
        with open("deletemock2.py") as file:
            exec(file.read())