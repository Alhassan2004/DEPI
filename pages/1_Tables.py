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

# --- Custom Styling (consistent and modern) ---
st.markdown("""
    <style>
    /* Background and text */
    .stApp {
        background-color: #FFFFFF;
        color: #1A1A1A;
    }

    /* Headers */
    h1, h2, h3 {
        text-align: center;
        color: #1E3A8A;  /* Deep blue */
        font-family: 'Arial', sans-serif;
    }

    /* Paragraphs, labels, and text */
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

    /* Select box styling */
    div[data-baseweb="select"] {
        color: #1E3A8A;
        font-weight: 600;
    }

    /* Section titles */
    .section-title {
        text-align: center;
        font-size: 22px;
        color: #2563EB; /* Blue accent */
        margin-top: 30px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Page Header ---
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

    # Filter valid tables
    options_to_show = [name for name in table_names if name in TABLE_DISPLAY_NAMES]

    if options_to_show:
        st.markdown("<h3 class='section-title'>📂 Select a Table</h3>", unsafe_allow_html=True)
        selected_table = st.selectbox(
            "",
            options=options_to_show,
            format_func=lambda name: TABLE_DISPLAY_NAMES.get(name, name),
            label_visibility="collapsed"
        )

        if selected_table:
            st.markdown(f"<h3 class='section-title'>🗂 Displaying Data for: {TABLE_DISPLAY_NAMES.get(selected_table)}</h3>", unsafe_allow_html=True)

            # Get all column names
            all_columns = conn.execute(f"PRAGMA table_info('{selected_table}')").fetchdf()
            column_names = all_columns['name'].tolist()

            # Filter out *_id columns
            columns_to_show = [name for name in column_names if not name.endswith('_id')]

            # Build query
            columns_string = ", ".join(columns_to_show)
            query = f"SELECT {columns_string} FROM {selected_table}"

            # Fetch data
            data_df = conn.execute(query).fetchdf()

            # Display dataframe
            st.dataframe(data_df, use_container_width=True)
    else:
        st.warning("⚠️ No tables found in the database. Please verify your 'job_postings.duckdb' file.")
else:
    st.stop()
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

# --- Custom Styling (consistent and modern) ---
st.markdown("""
    <style>
    /* Background and text */
    .stApp {
        background-color: #FFFFFF;
        color: #1A1A1A;
    }

    /* Headers */
    h1, h2, h3 {
        text-align: center;
        color: #1E3A8A;  /* Deep blue */
        font-family: 'Arial', sans-serif;
    }

    /* Paragraphs, labels, and text */
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

    /* Select box styling */
    div[data-baseweb="select"] {
        color: #1E3A8A;
        font-weight: 600;
    }

    /* Section titles */
    .section-title {
        text-align: center;
        font-size: 22px;
        color: #2563EB; /* Blue accent */
        margin-top: 30px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Page Header ---
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

    # Filter valid tables
    options_to_show = [name for name in table_names if name in TABLE_DISPLAY_NAMES]

    if options_to_show:
        st.markdown("<h3 class='section-title'>📂 Select a Table</h3>", unsafe_allow_html=True)
        selected_table = st.selectbox(
            "",
            options=options_to_show,
            format_func=lambda name: TABLE_DISPLAY_NAMES.get(name, name),
            label_visibility="collapsed"
        )

        if selected_table:
            st.markdown(f"<h3 class='section-title'>🗂 Displaying Data for: {TABLE_DISPLAY_NAMES.get(selected_table)}</h3>", unsafe_allow_html=True)

            # Get all column names
            all_columns = conn.execute(f"PRAGMA table_info('{selected_table}')").fetchdf()
            column_names = all_columns['name'].tolist()

            # Filter out *_id columns
            columns_to_show = [name for name in column_names if not name.endswith('_id')]

            # Build query
            columns_string = ", ".join(columns_to_show)
            query = f"SELECT {columns_string} FROM {selected_table}"

            # Fetch data
            data_df = conn.execute(query).fetchdf()

            # Display dataframe
            st.dataframe(data_df, use_container_width=True)
    else:
        st.warning("⚠️ No tables found in the database. Please verify your 'job_postings.duckdb' file.")
else:
    st.stop()

