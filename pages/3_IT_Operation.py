import streamlit as st
import pandas as pd
from Database.data_management import connect_db, get_all_tickets

# Access control
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()

st.set_page_config(page_title="IT Operations Dashboard", layout="wide")
st.title("IT Operations Dashboard")

# Load data
conn = connect_db()
rows = get_all_tickets(conn)
conn.close()

# Build DataFrame with correct columns
df = pd.DataFrame(rows, columns=[
    "Ticket ID", "Priority", "Description", "Status", "Assigned To", "Created At", "Resolution Time"
])

# Sidebar filter
st.sidebar.header("Filter Tickets")
status_filter = st.sidebar.multiselect(
    "Select Status",
    df["Status"].unique(),
    default=df["Status"].unique()
)

priority_filter = st.sidebar.multiselect(
    "Select Priority",
    df["Priority"].unique(),
    default=df["Priority"].unique()
)

# Apply filters
filtered_df = df[
    df["Status"].isin(status_filter) & df["Priority"].isin(priority_filter)
]

# Metrics
st.metric("Total Tickets", len(df))
st.metric("Filtered Tickets", len(filtered_df))

# Charts
if not filtered_df.empty:
    st.subheader("Ticket Priorities")
    st.bar_chart(filtered_df['Priority'].value_counts())

# Table
st.subheader("Ticket Records")
st.dataframe(filtered_df, use_container_width=True)
