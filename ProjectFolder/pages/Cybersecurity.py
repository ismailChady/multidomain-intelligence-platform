import streamlit as st
import pandas as pd
import os

st.title("Cybersecurity Domain")

# Ensuring the user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()

# Display welcome message
st.subheader(f"Welcome {st.session_state.username} to the Cybersecurity Dashboard")

# Load and display data
data_file = "Data/cybersecurity_data.csv"

if os.path.exists(data_file):
    df = pd.read_csv(data_file)
    st.write("### Cybersecurity Insights")
    st.dataframe(df)
else:
    st.error("Cybersecurity data not available. Please upload the dataset.")