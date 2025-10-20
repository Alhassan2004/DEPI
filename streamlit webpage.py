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
    <div style="font-size:22px; line-height:1.8; text-align:center; color:#2C3E50;">
        <b>Here you can:</b><br>
        📋 Explore job postings data (Tables page)<br>
        📊 Visualize job trends and insights (coming next)<br>
        🧠 Analyze skill requirements and career trends (future pages)<br><br>
        <i>Use the sidebar to navigate between pages.</i>
    </div>
""", unsafe_allow_html=True)


