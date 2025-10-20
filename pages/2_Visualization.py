import streamlit as st
import duckdb
import pandas as pd
import os

# --- Page Setup ---
st.set_page_config(
    page_title="Data Visualizations",
    layout="wide",
    page_icon="📊"
)

# --- Custom Styling (Same as your other pages) ---
st.markdown("""
    <style>
    /* Titles */
    h1, h2, h3 {
        text-align: center;
        color: #1E3A8A; /* Blue title color */
        font-family: 'Arial', sans-serif;
    }

    /* Section title */
    .section-title {
        text-align: center;
        font-size: 22px;
        color: #2563EB; /* Lighter blue for section titles */
        margin-top: 30px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>📊 Data Visualizations</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Select a category to visualize the count of job postings.</p>", unsafe_allow_html=True)

# --- Database Connection (Same as your table viewer page) ---
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

# --- Data Query Function ---
@st.cache_data
def run_query(_conn, query):
    """ Runs a SQL query and returns a DataFrame. """
    try:
        data_df = _conn.execute(query).fetchdf()
        return data_df
    except Exception as e:
        st.error(f"Error running query: {e}")
        return pd.DataFrame()

# --- Main App Logic ---
conn = get_connection()
if conn:
    st.markdown("<h3 class='section-title'>Select an Analysis</h3>", unsafe_allow_html=True)

    # --- Define the analyses ---
    # The user chooses one of these, and we run the corresponding query
    analysis_options = {
        "Top 15 Companies by Job Postings": {
            "query": """
                SELECT c.company_name, COUNT(j.job_id) AS quantity
                FROM fact_job_postings AS j
                JOIN dim_company AS c ON j.company_id = c.company_id
                GROUP BY c.company_name
                ORDER BY quantity DESC
                LIMIT 15
            """,
            "x_axis": "company_name"
        },
        "Top 15 Skills in Demand": {
            "query": """
                SELECT s.skill_name, COUNT(fjs.job_id) AS quantity
                FROM fact_job_posting_skill AS fjs
                JOIN dim_skills AS s ON fjs.skill_id = s.skill_id
                GROUP BY s.skill_name
                ORDER BY quantity DESC
                LIMIT 15
            """,
            "x_axis": "skill_name"
        },
        "Top 15 Job Locations": {
            "query": """
                SELECT l.location, COUNT(j.job_id) AS quantity
                FROM fact_job_postings AS j
                JOIN dim_location AS l ON j.location_id = l.location_id
                GROUP BY l.location
                ORDER BY quantity DESC
                LIMIT 15
            """,
            "x_axis": "location"
        }
    }

    # --- Create the dropdown ---
    selected_analysis_name = st.selectbox(
        label="Choose a chart to display:",
        options=analysis_options.keys(),
        label_visibility="collapsed"
    )

    if selected_analysis_name:
        # Get the query and x-axis details for the selected analysis
        analysis_details = analysis_options[selected_analysis_name]
        query = analysis_details["query"]
        x_col = analysis_details["x_axis"]
        
        # Run the query
        data_df = run_query(conn, query)

        # --- Display the chart and data ---
        if not data_df.empty:
            st.markdown(f"<h3 class='section-title'>{selected_analysis_name}</h3>", unsafe_allow_html=True)
            
            # Display the bar chart
            # We set the x-axis to our category (e.g., 'company_name')
            # and the y-axis to 'quantity'
            st.bar_chart(data_df, x=x_col, y="quantity")
            
            # Also display the raw data in a table
            st.dataframe(data_df, use_container_width=True)
        else:
            st.warning("No data found for this analysis.")
else:
    # This message shows if get_connection() failed
    st.error("Database connection could not be established.")
    st.stop()
