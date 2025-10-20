import streamlit as st
import duckdb
import pandas as pd
import os

# --- Page Layout Design ---
st.set_page_config(
    page_title="Job Postings Explorer",
    layout="wide",
    page_icon="📋"
)

# --- Custom Styling (same as Dashboard page) ---
st.markdown("""
    <style>
    .stApp {
        background-color: white;
        color: #2C3E50;
    }
    h1, h2, h3 {
        text-align: center;
        color: #2C3E50;
    }
    p, div, label {
        color: #2C3E50 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Page Header ---
st.markdown("<h1>📋 Job Postings Database Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Select a table from the database to view its contents.</p>", unsafe_allow_html=True)

# --- Database Connection ---
@st.cache_resource
def get_connection():
    # Get absolute path to ensure it works on Streamlit Cloud
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

# --- Connect and Load Tables ---
conn = get_connection()
if conn:
    table_names = get_table_names(conn)

    # Table Display Names
    TABLE_DISPLAY_NAMES = {
        "fact_job_postings": "All Job Postings",
        "dim_skills": "Skills Information",
        "dim_company": "Company Information",
        "dim_location": "Location Information",
        "dim_date": "Date Information"
    }

    # Filter the database tables to only include the ones we want to show
    options_to_show = [name for name in table_names if name in TABLE_DISPLAY_NAMES]

    if options_to_show:
        selected_table = st.selectbox(
            "Select a table",
            options=options_to_show,
            format_func=lambda name: TABLE_DISPLAY_NAMES.get(name, name),
            label_visibility="collapsed"
        )

        if selected_table:
            st.markdown(f"### Displaying data for: `{TABLE_DISPLAY_NAMES.get(selected_table)}`")

            # Get all column names for the selected table
            all_columns = conn.execute(f"PRAGMA table_info('{selected_table}')").fetchdf()
            column_names = all_columns['name'].tolist()

            # Filter out columns that end with '_id'
            columns_to_show = [name for name in column_names if not name.endswith('_id')]

            # Build the query with specific columns instead of '*'
            columns_string = ", ".join(columns_to_show)
            query = f"SELECT {columns_string} FROM {selected_table}"

            # Execute and display data
            data_df = conn.execute(query).fetchdf()
            st.dataframe(data_df, use_container_width=True)
    else:
        st.warning("⚠️ No tables found in the database. Please verify your 'job_postings.duckdb' file.")
else:
    st.stop()
