import streamlit as st

# --- Page Setup ---
st.set_page_config(
    layout="wide",
    page_icon="💼"
)

# --- Custom Styling ---
# We only style the title color, letting the default dark theme handle the rest.
st.markdown("""
    <style>
    h1, h2, h3 {
        text-align: center;
        color: #1E3A8A; /* Blue title color for consistency */
    }
    </style>
""", unsafe_allow_html=True)

# --- Page Title ---
st.markdown("<h1>💼 Intelligent Career Advisor Dashboard</h1>", unsafe_allow_html=True)

# --- Main Description Section ---
# Removed the inline "color:#2C3E50;" style to let the dark theme apply
st.markdown("""
    <div style="font-size:22px; line-height:1.8; text-align:center;">
        <b>Here you can:</b><br>
        1) Explore job postings data<br>
        2) Visualize job trends and insights<br>
        3) Analyze skill requirements and career trends<br><br>
        <i>Use the sidebar to navigate between pages.</i>
    </div>
""", unsafe_allow_html=True)

# --- Footer (Project Credits) ---
# Removed the inline "color:#2C3E50;" style here too
st.markdown("""
    <hr style="margin-top:40px; margin-bottom:10px;">
    <div style="text-align:center; font-size:18px;">
        <b>DEPI Round 3 Graduation Project</b><br>
        (Mohammed Morsi - Alhassan Soliman - Yassin Harraz - Maha Khaled - Youstina Nader - Menna El Naiad)
    </div>
""", unsafe_allow_html=True)
