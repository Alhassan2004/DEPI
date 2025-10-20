import streamlit as st
import duckdb
import pandas as pd
import os

st.set_page_config(
    page_title="Job Postings Explorer",
    layout="wide",
    page_icon="📋"
)

st.markdown("""
    <style>
    h1, h2, h3 {
        text-align: center;
        color: #1E3A8A;
        font-family: 'Arial', sans-serif;
    }

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

st.markdown("<h1>📋 Job Postings Database Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Select a table from the database to view its contents.</p>", unsafe_allow_html=True)

@st.cache_resource
def get_connection():
    db_path = "job_postings.duckdb"
    alt_db_path = os.path.join(os.path.dirname(__file__), "..", "job_postings.duckdb")

    if os.path.exists(db_path):
        db_to_use = db_path
    elif os.path.exists(alt_db_path):
        db_to_use = alt_db_path
    else:
        st.error(f"❌ Database file not found. Tried: '{db_path}' and '{alt_db_path}'")
        return None

    try:
        conn = duckdb.connect(database=db_to_use, read_only=True)
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

conn = get_connection()
if conn:
    all_table_names = get_table_names(conn)

    TABLE_DISPLAY_NAMES = {
        "fact_job_postings": "All Job Postings",
        "dim_skills": "Skills Information",
        "dim_company": "Company Information",
        "dim_location": "Location Information",
        "dim_date": "Date Information"
    }

    tables_to_hide = [
        "fact_job_posting_skill",
        "raw_job_postings",
        "stg_job_postings"
    ]

    options_to_show = [name for name in all_table_names if name not in tables_to_hide]

    if options_to_show:
        st.markdown("<h3 class='section-title'>📂 Select a Table</h3>", unsafe_allow_html=True)

        selected_table = st.selectbox(
            label="Select a table",
            options=options_to_show,
            format_func=lambda name: TABLE_DISPLAY_NAMES.get(name, name.replace("_", " ").title()),
            label_visibility="collapsed"
        )

        if selected_table:
            display_name = TABLE_DISPLAY_NAMES.get(selected_table, selected_table.replace('_', ' ').title())
            st.markdown(f"<h3 class='section-title'>Displaying Data for: {display_name}</h3>", unsafe_allow_html=True)

            try:
                all_columns = conn.execute(f"PRAGMA table_info('{selected_table}')").fetchdf()
                column_names = all_columns['name'].tolist()

                columns_to_show = [name for name in column_names if not name.endswith('_id')]
                columns_string = ", ".join(f'"{name}"' for name in columns_to_show)

                query = f"SELECT {columns_string} FROM {selected_table} LIMIT 1000"

                data_df = conn.execute(query).fetchdf()
                st.dataframe(data_df, use_container_width=True)

            except Exception as e:
                st.error(f"Error loading table '{selected_table}': {e}")

    else:
        st.warning("⚠️ No tables found to display. Please verify your 'job_postings.duckdb' file.")
else:
    st.error("Database connection could not be established.")
    st.stop()
