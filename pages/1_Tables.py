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
    /* 1. Overall Page Style */
    .stApp {
        background-color: #F9F9F9; /* Off-white background */
        color: #000000;         /* Default black text */
    }

    /* 2. Titles (Kept from your original request) */
    h1, h2, h3 {
        text-align: center;
        color: #1E3A8A; /* Blue title color */
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
    
    /* 3. General Text (Ensures it's black) */
    p, div, label, span {
        color: #000000 !important;
    }

    /* 4. DROPDOWN (Selectbox) STYLING */
    
    /* The main box *before* clicking */
    div[data-baseweb="select"] > div {
        background-color: #F9F9F9 !important;    /* Off-white */
        color: #000000 !important;              /* Black text */
        border: 1px solid #D1D5DB !important;  /* Light grey border */
    }

    /* The text *inside* the main box */
    div[data-baseweb="select"] span {
        color: #000000 !important;
    }

    /* The dropdown arrow */
    div[data-baseweb="select"] svg {
        fill: #000000 !important;
    }

    /* 5. DROPDOWN *LIST* STYLING (The popover) */
    
    /* This targets items in the expanded list (for Light and Dark themes) */
    [data-theme="light"] div[data-baseweb="popover"] li[role="option"],
    [data-theme="dark"] div[data-baseweb="popover"] li[role="option"] {
        background-color: #F9F9F9 !important;    /* Off-white */
        color: #000000 !important;              /* Black text */
    }

    /* The *hovered* item in the list */
    [data-theme="light"] div[data-baseweb="popover"] li[role="option"]:hover,
    [data-theme="dark"] div[data-baseweb="popover"] li[role="option"]:hover {
        background-color: #EDEDED !important;    /* Slightly darker off-white */
        color: #000000 !important;
    }
    
    /* The *selected* item in the list */
    [data-theme="dark"] div[data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #D1D5DB !important;    /* Medium grey for selected */
        color: #000000 !important;
    }

    /* 6. DATAFRAME (Table) STYLING */
    .stDataFrame {
        background-color: #F9F9F9; /* Off-white container */
        border: 1px solid #D1D5DB;
        border-radius: 8px;
    }
    /* Ensure dataframe text is black */
    .stDataFrame div {
         color: #000000 !important;
    }
    /* Dataframe header */
    [data-testid="stHeader"] {
        background-color: #EDEDED; /* Light grey header */
        color: #000000;
    }
    
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>📋 Job Postings Database Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Select a table from the database to view its contents.</p>", unsafe_allow_html=True)

# --- Database Connection ---
@st.cache_resource
def get_connection():
    # Use a relative path to find the database
    # Assumes db is in the parent folder (e.g., main repo folder)
    # and this script is in a subfolder (e.g., /pages)
    # If a.py and db are in the SAME folder, just use "job_postings.duckdb"
    db_path = "job_postings.duckdb" 
    
    # This logic tries to find it in the parent folder, good for Streamlit Cloud
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

# --- Main App Logic ---
conn = get_connection()
if conn:
    all_table_names = get_table_names(conn)

    # --- Configuration for Table Names ---
    
    # 1. Pretty names for known tables
    TABLE_DISPLAY_NAMES = {
        "fact_job_postings": "All Job Postings",
        "dim_skills": "Skills Information",
        "dim_company": "Company Information",
        "dim_location": "Location Information",
        "dim_date": "Date Information"
    }

    # 2. Tables to HIDE from the dropdown
    tables_to_hide = [
        "fact_job_posting_skill", 
        "raw_job_postings", 
        "stg_job_postings"
    ]
    
    # 3. Create the final list of options
    options_to_show = [name for name in all_table_names if name not in tables_to_hide]
    # --- End Configuration ---

    if options_to_show:
        st.markdown("<h3 class='section-title'>📂 Select a Table</h3>", unsafe_allow_html=True)

        # Create the dropdown menu
        selected_table = st.selectbox(
            label="Select a table", # Label is needed but hidden
            options=options_to_show,
            format_func=lambda name: TABLE_DISPLAY_NAMES.get(name, name.replace("_", " ").title()),
            label_visibility="collapsed"
        )

        # --- Display the Selected Table ---
        if selected_table:
            display_name = TABLE_DISPLAY_NAMES.get(selected_table, selected_table.replace('_', ' ').title())
            st.markdown(f"<h3 class='section-title'>Displaying Data for: {display_name}</h3>", unsafe_allow_html=True)

            try:
                # Get all column names for the selected table
                all_columns = conn.execute(f"PRAGMA table_info('{selected_table}')").fetchdf()
                column_names = all_columns['name'].tolist()

                # Filter out any columns that end in '_id'
                columns_to_show = [name for name in column_names if not name.endswith('_id')]
                columns_string = ", ".join(f'"{name}"' for name in columns_to_show) # Add quotes for safety

                # Build the query
                query = f"SELECT {columns_string} FROM {selected_table} LIMIT 1000" # Limit to 1000 rows for performance

                # Fetch and display data
                data_df = conn.execute(query).fetchdf()
                st.dataframe(data_df, use_container_width=True)
            
            except Exception as e:
                st.error(f"Error loading table '{selected_table}': {e}")

    else:
        st.warning("⚠️ No tables found to display. Please verify your 'job_postings.duckdb' file.")
else:
    # This message shows if get_connection() failed
    st.error("Database connection could not be established.")
    st.stop()
