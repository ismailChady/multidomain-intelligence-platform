import streamlit as st
from Login import login_user, register_user

st.set_page_config(page_title="Login / Register", layout="centered")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# If already logged in, show shortcut
if st.session_state.logged_in:
    st.success(f"Welcome back, {st.session_state.username}!")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Cybersecurity.py")  # Or 4_Dashboard.py
    st.stop()

st.title(" Welcome to the Intelligence Platform")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    success = login_user()
    if success:
        st.success(f"Welcome {st.session_state.username}!")
        st.switch_page("pages/1_Cybersecurity.py")  # Or redirect to dashboard

with tab2:
    register_user()