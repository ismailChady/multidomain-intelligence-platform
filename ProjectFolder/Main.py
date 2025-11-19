import streamlit as st

#import Login function
from Login import register_user, login_user

#Pandas for data handling
import pandas as pd
import os
st.set_page_config(
    page_title="Multidomain-intelligence-platform",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Multidomain Intelligence Platform")
st.write("Welcome to the Multidomain Intelligence Platform. This platform supports Cybersecurity, IT Operations, and Data Science insights.")

#Sidebar for navigation menu
menu = ["Home", "Login", "Register"]
choice = st.sidebar.selectbox("Navigation", menu)

#intializing session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
    #Registration page
if choice == "Register":
    st.subheader("Create New Account")
    if st.button("Register"):
        register_user()
#Login page
elif choice == "Login":
    st.subheader("Login to Your Account")
    if st.button("Login"):
        if login_user():
            st.session_state.logged_in = True
            st.success("Login successful!")
#Home page
elif choice == "Home":
    if st.session_state.logged_in:
        st.subheader(f"Welcome {st.session_state.username} to the Multidomain Intelligence Platform")
    else:
        st.subheader("Please login or register to access the platform features.")
    if st.session_state.logged_in:
        domain = st.selectbox("Select Domain", ["Cybersecurity", "IT Operations", "Data Science"])
        if domain == "Cybersecurity":
            st.subheader("Cybersecurity Insights")
            if os.path.exists("Data/cybersecurity_data.csv"):
                df = pd.read_csv("Data/cybersecurity_data.csv")
                st.dataframe(df)
            else:
                st.error("Cybersecurity data not available.")

        elif domain == "IT Operations": 
            st.subheader("IT Tickets")
            if os.path.exists("Data/it_tickets.csv"):
                df = pd.read_csv("Data/it_tickets.csv")
                st.dataframe(df)
            else:
                st.error("IT Tickets dataset not available.")

        elif domain == "Data Science":
            st.subheader("Dataset Metadata")
            if os.path.exists("Data/dataset_metadata.csv"):
                df = pd.read_csv("Data/dataset_metadata.csv")
                st.dataframe(df)
            else:
                st.error("Dataset metadata not available.")

