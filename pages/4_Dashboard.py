import streamlit as st
import pandas as pd
from Database.data_management import connect_db, get_all_incidents, get_all_tickets, get_all_datasets

#ACCESS CONTROL
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()

st.set_page_config(page_title="Global Summary Dashboard", layout="wide")
st.title("Global Summary Dashboard")

#LOAD DATA
conn = connect_db()
cyber = pd.DataFrame(get_all_incidents(conn), columns=[
    "incident_id", "timestamp", "severity", "category", "status", "description"
])
tickets = pd.DataFrame(get_all_tickets(conn), columns=[
    "ticket_id", "priority", "description", "status", "assigned_to", "created_at", "resolution_time_hours"
])
datasets = pd.DataFrame(get_all_datasets(conn), columns=[
    "dataset_id", "name", "source", "category", "size", "uploaded_by", "upload_date"
])
conn.close()

#OVERVIEW METRICS
st.subheader("Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Cyber Incidents", len(cyber))
col2.metric("IT Tickets", len(tickets))
col3.metric("Datasets", len(datasets))

st.divider()

#CHARTS
st.subheader("Summary Charts")
col4, col5 = st.columns(2)

with col4:
    if not cyber.empty and "status" in cyber.columns:
        st.markdown("**Cybersecurity: Status Distribution**")
        st.bar_chart(cyber["status"].value_counts())

with col5:
    if not tickets.empty and "priority" in tickets.columns:
        st.markdown("**IT Tickets: Priority Distribution**")
        st.bar_chart(tickets["priority"].value_counts())

if not datasets.empty and "category" in datasets.columns:
    st.markdown("**📁 Dataset Categories**")
    st.bar_chart(datasets["category"].value_counts())

st.divider()

#TABLES
st.subheader("Recent Records")

st.markdown("**Latest Cyber Incidents**")
if not cyber.empty:
    cyber["timestamp"] = pd.to_datetime(cyber["timestamp"], errors="coerce")
    st.dataframe(cyber.sort_values("timestamp", ascending=False).head(5), use_container_width=True)

st.markdown("**Latest IT Tickets**")
if not tickets.empty:
    tickets["created_at"] = pd.to_datetime(tickets["created_at"], errors="coerce")
    st.dataframe(tickets.sort_values("created_at", ascending=False).head(5), use_container_width=True)

st.markdown("**Latest Uploaded Datasets**")
if not datasets.empty:
    datasets["upload_date"] = pd.to_datetime(datasets["upload_date"], errors="coerce")
    st.dataframe(datasets.sort_values("upload_date", ascending=False).head(5), use_container_width=True)