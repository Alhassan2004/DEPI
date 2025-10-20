import streamlit as st

# --- Page Setup ---
st.set_page_config(
    page_title="Job Postings Explorer",
    layout="wide",
    page_icon="💼"
)

# --- Custom Styling ---
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

# --- Page Content ---
st.markdown("<h1>💼 Intelligent Career Advisor Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
Welcome to the **Job Postings Explorer** platform.  
Here you can:
- 📋 Explore job postings data (Tables page)
- 📊 Visualize job trends and insights (coming next)
- 🧠 Analyze skill requirements and career trends (future pages)

Use the sidebar to navigate between pages.
""")


