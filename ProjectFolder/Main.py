import streamlit as st

# Configure page
st.set_page_config(
    page_title="Multidomain Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Welcome title
st.title("Multidomain Intelligence Platform")

# Introduction text
st.write("""
Welcome to the **Multidomain Intelligence Platform**.

This platform provides:
-  User Authentication (Register/Login)
-  Cybersecurity Insights
-  IT Operations Analytics
-  Data Science Metadata Exploration

 Please use the sidebar to navigate between sections.
""")