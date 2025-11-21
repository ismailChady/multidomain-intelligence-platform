import streamlit as st
import pandas as pd
from Database.data_management import connect_db, get_all_incidents


# Access control
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()

st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")
st.title("Cybersecurity Incident Dashboard")

# Sidebar filters
st.sidebar.header("Filter Incidents")
status_filter = st.sidebar.multiselect(
    "Select Status",
    ["open", "closed", "investigating"],
    default=["open", "closed", "investigating"]
)

severity_filter = st.sidebar.multiselect(
    "Select Severity",
    ["Low", "Medium", "High", "Critical"],
    default=["Low", "Medium", "High", "Critical"]
)

# Load data
conn = connect_db()
rows = get_all_incidents(conn)
conn.close()

# Convert to DataFrame
df = pd.DataFrame(rows, columns=["ID", "Title", "Severity", "Status", "Date"])

# Filter
filtered_df = df[
    df["Status"].isin(status_filter) &
    df["Severity"].isin(severity_filter)
]

# Metrics
st.metric("Total Incidents", len(df))
st.metric("Filtered", len(filtered_df))

# Charts
if not filtered_df.empty:
    st.subheader("Incidents Over Time")
    chart_df = filtered_df.groupby("Date").size().reset_index(name="Incidents")
    st.line_chart(chart_df.rename(columns={"Date": "index"}).set_index("index"))

# Table
st.subheader("Incident Records")
st.dataframe(filtered_df, use_container_width=True)