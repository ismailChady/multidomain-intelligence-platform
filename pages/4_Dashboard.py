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

st.title("Global Summary Dashboard")

cyber, tickets, datasets = load_data()

# Overview counts
st.header("Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Cyber Incidents", len(cyber))
col2.metric("IT Tickets", len(tickets))
col3.metric("Datasets", len(datasets))

st.divider()

# Charts
st.subheader("Cybersecurity Status Distribution")
if "status" in cyber.columns:
    st.bar_chart(cyber["status"].value_counts())

st.subheader("IT Ticket Priorities")
if "priority" in tickets.columns:
    st.bar_chart(tickets["priority"].value_counts())

st.subheader("Dataset Categories")
if "category" in datasets.columns:
    st.bar_chart(datasets["category"].value_counts())

st.divider()

# Tables
st.subheader("Latest Incidents")
if "timestamp" in cyber.columns:
    st.dataframe(cyber.sort_values("timestamp", ascending=False).head(5))

st.subheader("Latest IT Tickets")
if "created_date" in tickets.columns:
    st.dataframe(tickets.sort_values("created_date", ascending=False).head(5))

st.subheader("Recently Uploaded Datasets")
st.dataframe(datasets.head(5))