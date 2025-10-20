import streamlit as st
import duckdb
import pandas as pd
import os
import altair as alt

st.set_page_config(
    page_title="Data Visualizations",
    layout="wide",
    page_icon="📊"
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

st.markdown("<h1>📊 Data Visualizations</h1>", unsafe_allow_html=True)

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
def run_query(_conn, query):
    """ Runs a SQL query and returns a DataFrame. """
    try:
        data_df = _conn.execute(query).fetchdf()
        return data_df
    except Exception as e:
        st.error(f"Error running query: {e}")
        return pd.DataFrame()

conn = get_connection()
if conn:
    st.markdown("<h3 class='section-title'>Select an Analysis</h3>", unsafe_allow_html=True)

    analysis_options = {
        "Companies by Job Postings": {
            "query": """
                SELECT c.company_name, COUNT(j.posting_id) AS quantity
                FROM fact_job_postings AS j
                JOIN dim_company AS c ON j.company_id = c.company_id
                GROUP BY c.company_name
                ORDER BY quantity DESC
            """,
            "x_axis": "company_name",
            "x_title": "Company Name"
        },
        "Skills in Demand": {
            "query": """
                SELECT s.skill_name, COUNT(fjs.posting_id) AS quantity
                FROM fact_job_posting_skill AS fjs
                JOIN dim_skills AS s ON fjs.skill_id = s.skill_id
                GROUP BY s.skill_name
                ORDER BY quantity DESC
            """,
            "x_axis": "skill_name",
            "x_title": "Skill Name"
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
             "x_axis": "location_full",
             "x_title": "Location"
        }
    }

    selected_analysis_name = st.selectbox(
        label="Choose a chart to display:",
        options=list(analysis_options.keys()),
        label_visibility="collapsed"
    )

    if selected_analysis_name:
        analysis_details = analysis_options[selected_analysis_name]
        query = analysis_details["query"]
        x_col = analysis_details["x_axis"]
        x_title = analysis_details["x_title"]
        y_col = "quantity"
        y_title = "Number of Job Postings"

        data_df = run_query(conn, query)

        if not data_df.empty:
            st.markdown(f"<h3 class='section-title'>{selected_analysis_name}</h3>", unsafe_allow_html=True)

            chart = alt.Chart(data_df).mark_bar().encode(
                x=alt.X(x_col, title=x_title, sort='-y'),
                y=alt.Y(y_col, title=y_title),
                tooltip=[x_col, y_col]
            ).properties(
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

            st.dataframe(data_df, use_container_width=True)
        else:
            st.warning("No data found for this analysis or an error occurred running the query.")
else:
    st.error("Database connection could not be established.")
    st.stop()
