import streamlit as st
import duckdb
import pandas as pd

# Page Layout Design
st.set_page_config(
    page_title="Job Postings Explorer",
    layout="wide"
)

TABLE_DISPLAY_NAMES = {
    "fact_job_postings": "All Job Postings",
    "dim_skills": "Skills Information",
    "dim_company": "Company Information",
    "dim_location": "Location Information",
    "dim_date": "Date Information"
}

st.title("Job Postings Database Explorer")
st.write("Select a table from the database to view its contents.")

# Database Connection
@st.cache_resource
def get_connection():
    conn = duckdb.connect(database='job_postings.duckdb', read_only=True)
    return conn

@st.cache_data
def get_table_names(_conn):
    tables = _conn.execute("SHOW ALL TABLES;").fetchdf()
    return tables['name'].tolist()

conn = get_connection()
table_names = get_table_names(conn)

# Filter the database tables to only include the ones we want to show
options_to_show = [name for name in table_names if name in TABLE_DISPLAY_NAMES]

# User Interface
selected_table = st.selectbox(
    "Select a table",
    options=options_to_show,
    format_func=lambda name: TABLE_DISPLAY_NAMES.get(name, name),
    label_visibility="collapsed"
)

if selected_table:
    st.markdown(f"### Displaying data for: `{TABLE_DISPLAY_NAMES.get(selected_table)}`")
    
    # --- FIX STARTS HERE ---

    # 1. Get all column names for the selected table
    all_columns = conn.execute(f"PRAGMA table_info('{selected_table}')").fetchdf()
    column_names = all_columns['name'].tolist()
    
    # 2. Filter out columns that end with '_id'
    columns_to_show = [name for name in column_names if not name.endswith('_id')]
    
    # 3. Create a string of the columns to show, separated by commas
    columns_string = ", ".join(columns_to_show)
    
    # 4. Build the final query with the specific columns instead of '*'
    query = f"SELECT {columns_string} FROM {selected_table}"
    
    data_df = conn.execute(query).fetchdf()
    st.dataframe(data_df, use_container_width=True)