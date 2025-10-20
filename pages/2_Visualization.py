import streamlit as st
import duckdb
import pandas as pd
import os
import altair as alt # Import Altair

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

    # --- Define the analyses (LIMIT removed) ---
    analysis_options = {
        "Companies by Job Postings": {
            "query": """
                SELECT c.company_name, COUNT(j.posting_id) AS quantity
                FROM fact_job_postings AS j
                JOIN dim_company AS c ON j.company_id = c.company_id
                GROUP BY c.company_name
                ORDER BY quantity DESC
            """,
            "y_axis": "company_name", # Renamed for clarity with Altair
            "y_title": "Company Name" # Title for the Y-axis
        },
        "Skills in Demand": {
            "query": """
                SELECT s.skill_name, COUNT(fjs.posting_id) AS quantity
                FROM fact_job_posting_skill AS fjs
                JOIN dim_skills AS s ON fjs.skill_id = s.skill_id
                GROUP BY s.skill_name
                ORDER BY quantity DESC
            """,
            "y_axis": "skill_name",
            "y_title": "Skill Name"
        },
        "Job Locations": {
            "query": """
                SELECT l.city || ', ' || l.governorate || ', ' || l.country AS location_full,
                       COUNT(j.posting_id) AS quantity
                FROM fact_job_postings AS j
                JOIN dim_location AS l ON j.location_id = l.location_id
                WHERE l.city IS NOT NULL AND l.governorate IS NOT NULL AND l.country IS NOT NULL
                GROUP BY location_full
                ORDER BY quantity DESC
            """,
             "y_axis": "location_full",
             "y_title": "Location"
        }
        # You can add more analyses here following the same pattern
    }

    # --- Create the dropdown ---
    selected_analysis_name = st.selectbox(
        label="Choose a chart to display:",
        options=list(analysis_options.keys()), # Ensure it's a list for compatibility
        label_visibility="collapsed"
    )

    if selected_analysis_name:
        # Get the query and axis details for the selected analysis
        analysis_details = analysis_options[selected_analysis_name]
        query = analysis_details["query"]
        y_col = analysis_details["y_axis"]
        y_title = analysis_details["y_title"]
        x_col = "quantity" # Quantity is always the X-axis now
        x_title = "Number of Job Postings" # Title for X-axis

        # Run the query
        data_df = run_query(conn, query)

        # --- Display the chart and data ---
        if not data_df.empty:
            st.markdown(f"<h3 class='section-title'>{selected_analysis_name}</h3>", unsafe_allow_html=True)

            # --- Create Horizontal Bar Chart with Altair ---
            chart = alt.Chart(data_df).mark_bar().encode(
                x=alt.X(x_col, title=x_title), # Quantity on X-axis
                y=alt.Y(y_col, title=y_title, sort='-x'), # Category on Y-axis, sorted by quantity descending
                tooltip=[y_col, x_col] # Show details on hover
            ).properties(
                 # title=selected_analysis_name # Optional: Title within the chart itself
            ).interactive() # Allow zooming and panning

            st.altair_chart(chart, use_container_width=True)
            # --- End Altair Chart ---

            # Also display the raw data in a table
            st.dataframe(data_df, use_container_width=True)
        else:
            st.warning("No data found for this analysis or an error occurred running the query.")
else:
    # This message shows if get_connection() failed
    st.error("Database connection could not be established.")
    st.stop()
