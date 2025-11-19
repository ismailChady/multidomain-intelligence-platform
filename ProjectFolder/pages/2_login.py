import streamlit as st
from Login import login_user

st.title("Login")

# Display login form using your existing login_user() function
if login_user():
    st.session_state.logged_in = True
    st.success(f"Welcome back, {st.session_state.username}!")