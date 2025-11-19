import streamlit as st
import pandas as pd
import os

st.title("Home - Multidomain Intelligence Platform")

# Initialize session variables if not present
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Show content based on login status
if st.session_state.logged_in:
    st.subheader(f"Welcome {st.session_state.username}!")
    st.write("Select a domain to view relevant insights.")

    domain = st.selectbox("Select Domain", ["Cybersecurity", "IT Operations", "Data Science"])

    if domain == "Cybersecurity":
        st.subheader("Cybersecurity Insights")
        data_path = "Data/cybersecurity_data.csv"
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            st.dataframe(df)
        else:
            st.error("Cybersecurity data not available.")

    elif domain == "IT Operations":
        st.subheader("IT Tickets")
        data_path = "Data/it_tickets.csv"
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            st.dataframe(df)
        else:
            st.error("IT Tickets dataset not available.")

    elif domain == "Data Science":
        st.subheader("Dataset Metadata")
        data_path = "Data/dataset_metadata.csv"
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            st.dataframe(df)
        else:
            st.error("Dataset metadata not available.")

else:
    st.warning("Please log in to access the platform.")