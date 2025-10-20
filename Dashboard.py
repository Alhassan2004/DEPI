import streamlit as st

# --- Page Setup ---
st.set_page_config(
    page_title="Dashboard",     # 👈 this changes the name in the sidebar
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

# --- Page Title ---
st.markdown("<h1>💼 Intelligent Career Advisor Dashboard</h1>", unsafe_allow_html=True)

# --- Main Description Section ---
st.markdown("""
    <div style="font-size:22px; line-height:1.8; text-align:center; color:#2C3E50;">
        <b>Here you can:</b><br>
         1) Explore job postings data (Tables page)<br>
         2) Visualize job trends and insights (coming next)<br>
         3) Analyze skill requirements and career trends (future pages)<br><br>
        <i>Use the sidebar to navigate between pages.</i>
    </div>
""", unsafe_allow_html=True)

# --- Footer (Project Credits) ---
st.markdown("""
    <hr style="margin-top:40px; margin-bottom:10px;">
    <div style="text-align:center; color:#2C3E50; font-size:18px;">
        <b>DEPI Round 3 Graduation Project</b><br>
        (Alhassan Soliman, Mohammed Morsi, Yassin Harraz, Maha Khaled, Youstina Nader, Menna El Niaad)
    </div>
""", unsafe_allow_html=True)


