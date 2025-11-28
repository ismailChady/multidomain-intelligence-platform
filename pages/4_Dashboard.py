import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "Data/intelligence_platform.db"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    cyber = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    tickets = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    datasets = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return cyber, tickets, datasets

# Access control
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()

st.set_page_config(page_title="Global Summary Dashboard", layout="wide")
st.title("Global Summary Dashboard")

#Load all 3 domain datasets
cyber_df, tickets_df, datasets_df = load_data()

# Metrics
st.header("Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Cyber Incidents", len(cyber_df))
col2.metric("IT Tickets", len(tickets_df))
col3.metric("Datasets", len(datasets_df))

st.divider()

# Charts
st.subheader("Cybersecurity Incident Status Distribution")
if "status" in cyber_df.columns:
    st.bar_chart(cyber_df["status"].value_counts())

st.subheader(" IT Ticket Priorities")
if "priority" in tickets_df.columns:
    st.bar_chart(tickets_df["priority"].value_counts())

st.subheader("Dataset Categories")
if "category" in datasets_df.columns:
    st.bar_chart(datasets_df["category"].value_counts())

st.divider()

#Recent Records Tables
st.subheader("Latest 5 Cyber Incidents")
if "timestamp" in cyber_df.columns:
    st.dataframe(cyber_df.sort_values("timestamp", ascending=False).head(5), use_container_width=True)

st.subheader("Latest 5 IT Tickets")
if "created_at" in tickets_df.columns:
    st.dataframe(tickets_df.sort_values("created_at", ascending=False).head(5), use_container_width=True)

st.subheader("Recently Uploaded Datasets")
st.dataframe(datasets_df.sort_values("upload_date", ascending=False).head(5), use_container_width=True)