import streamlit as st
import duckdb
import pandas as pd
import os

# --- Page Setup ---
st.set_page_config(
    page_title="Job Postings Explorer",
    layout="wide",
    page_icon="📋"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background-color: #FFFFFF;
        color: #1A1A1A;
        font-family: 'Arial', sans-serif;
    }

    /* Titles */
    h1, h2, h3 {
        text-align: center;
        color: #1E3A8A;
        font-family: 'Arial', sans-serif;
    }

    /* Paragraphs and labels */
    p, div, label {
        color: #1A1A1A !important;
        font-family: 'Arial', sans-serif;
    }

    /* DataFrame appearance */
    .stDataFrame {
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        background-color: #F9FAFB;
    }

    /* Fix dropdown colors (selectbox) */
    div[data-baseweb="select"] > div {
        background-color: #F0F4FF !important;
        color: #1E3A8A !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #1E3A8A !important;
    }
    div[data-baseweb="select"] span {
        color: #1E3A8A !important;
    }

    /* Hover state for dropdown */
    div[data-baseweb="select"] div:hover {
        background-color: #DBEAFE !important;
        color: #1E3A8A !important;
    }

    /* Section title */
    .section-title {
        text-align: center;
        font-size: 22px;
        color: #2563EB;
        margin-top: 30px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>📋 Job Postings Database Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Select a table from the database to view its contents.</p>", unsafe_allow_html=True)

# --- Database Connection ---
@st.cache_resource
def get_connection():
    db_path = os.path.join(os.path.dirname(__file__), "..", "job_postings.duckdb")
    if not os.path.exists(db_path):
        st.error("❌ Database file not found. Make sure 'job_postings.duckdb' exists in the main project folder.")
        return None
    try:
        conn = duckdb.connect(database=db_path, read_only=True)
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

@st.cache_data
def get_table_names(_conn):
    try:
        tables = _conn.execute("SHOW ALL TABLES;").fetchdf()
        return tables['name'].tolist()
    except Exception as e:
        st.error(f"Error fetching tables: {e}")
        return []

# --- Connect & Load ---
conn = get_connection()
if conn:
    table_names = get_table_names(conn)

    TABLE_DISPLAY_NAMES = {
        "fact_job_postings": "All Job Postings",
        "dim_skills": "Skills Information",
        "dim_company": "Company Information",
        "dim_location": "Location Information",
        "dim_date": "Date Information"
    }

    options_to_show = [name for name in table_names if name in TABLE_DISPLAY_NAMES]

    if options_to_show:
        st.markdown("<h3 class='section-title'>📂 Select a Table</h3>", unsafe_allow_html=True)
        se


