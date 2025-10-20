import streamlit as st

st.set_page_config(
    layout="wide",
    page_icon="💼"
)

st.markdown("""
    <style>
    h1, h2, h3 {
        text-align: center;
        color: #1E3A8A; /* Blue title color for consistency */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Intelligent Career Advisor Dashboard</h1>", unsafe_allow_html=True)

st.markdown("""
    <div style="font-size:22px; line-height:1.8; text-align:center;">
        <b>Here you can:</b><br>
        1) Explore job postings data<br>
        2) Visualize job trends and insights<br>
        3) Analyze skill requirements and career trends<br><br>
        <i>Use the sidebar to navigate between pages.</i>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <hr style="margin-top:40px; margin-bottom:10px;">
    <div style="text-align:center; font-size:18px;">
        <b>DEPI Round 3 Graduation Project</b><br>
    </div>
""", unsafe_allow_html=True)
