import streamlit as st
import duckdb
import pandas as pd

# --- Page Layout Design ---
st.set_page_config(
    page_title="Job Postings Explorer",
    layout="wide",
    page_icon="📋"
)

# --- Custom Styling (same as dashboard) ---
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
    </style>
""", unsafe_allow_html=True)

# --- Page Header ---
st.markdown("<h1>📋 Job Postings Database Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#2C3E50;'>Select a table from the database to view its contents.</p>", unsafe_allow_html=True)

# --- Database Connection ---
@st.cache_resource
def get_connection():
    conn = duckdb.connect(database='job_postings.duckdb', read_only=True)
