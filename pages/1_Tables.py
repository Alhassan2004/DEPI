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
    /* Background and font */
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

    /* DataFrame container */
    .stDataFrame {
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        background-color: #F9FAFB;
    }

    /* --- DROPDOWN (Selectbox) COLORS --- */
    
    /* This targets the main box you see *before* clicking */
    div[data-baseweb="select"] > div {
        background-color: #F9F9F9 !important;    /* Off-white background */
        color: #000000 !important;              /* Black text */
        font-weight: 500 !important;
        border-radius: 6px !important;
        border: 1px solid #D1D5DB !important;  /* Added a light border */
    }

    /* This targets the text *inside* the main box */
    div[data-baseweb="select"] span {
        color: #000000 !important;              /* Black text */
    }

    /* This targets the dropdown arrow icon */
    div[data-baseweb="select"] svg {
        fill: #000000 !important;              /* Black arrow */
    }

    /* --- This is the CORRECTED part --- */
    
    /* This targets the items in the *expanded list* */
    div[data-baseweb="popover"] li[role="option"] {
        background-color: #F9F9F9 !important;    /* Off-white background */
        color: #000000 !important;              /* Black text */
    }

    /* This targets the *hovered* items in the list */
    div[data-baseweb="popover"] li[role="option"]:hover {
        background-color: #EDEDED !important;    /* Slightly darker off-white */
        color: #000000 !important;
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
    # Get absolute path (works both locally and on Streamlit Cloud)
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

# --- Connect and Load ---
conn = get_connection()
if conn:
    table_names = get_table_names(conn)

    # Known display names
    TABLE_DISPLAY_NAMES = {
        "fact_job_postings": "All Job Postings",
        "dim_skills": "Skills Information",
        "dim_company": "Company Information",
        "dim_location": "Location Information",
        "dim_date": "Date Information"
    }

    # ✅ Show all tables, not just filtered ones
    options_to_show = table_names

    if options_to_show:
        st.markdown("<h3 class='section-title'>📂 Select a Table</h3>", unsafe_allow_html=True)

        selected_table = st.selectbox(
            "",
            options=options_to_show,
            # Show pretty names for known tables, readable names for others
            format_func=lambda name: TABLE_DISPLAY_NAMES.get(name, name.replace("_", " ").title()),
            label_visibility="collapsed"
        )

        if selected_table:
            st.markdown(f"<h3 class='section-title'>🗂 Displaying Data for: {TABLE_DISPLAY_NAMES.get(selected_table, selected_table.replace('_', ' ').title())}</h3>", unsafe_allow_html=True)

            # Get all column names
            all_columns = conn.execute(f"PRAGMA table_info('{selected_table}')").fetchdf()
            column_names = all_columns['name'].tolist()

            # Filter out *_id columns
            columns_to_show = [name for name in column_names if not name.endswith('_id')]

            # Build query
            columns_string = ", ".join(columns_to_show)
            query = f"SELECT {columns_string} FROM {selected_table}"

            # Fetch and display data
            data_df = conn.execute(query).fetchdf()
            st.dataframe(data_df, use_container_width=True)
    else:
        st.warning("⚠️ No tables found in the database. Please verify your 'job_postings.duckdb' file.")
else:
    st.stop()
