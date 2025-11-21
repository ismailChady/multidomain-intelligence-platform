import streamlit as st
import pandas as pd
from Database.data_management import connect_db, get_all_datasets

# Access control
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()

st.set_page_config(page_title="Data Science Dashboard", layout="wide")
st.title("🧠 Data Science Dashboard")

# Load data
conn = connect_db()
rows = get_all_datasets(conn)
conn.close()

# Build DataFrame (corrected columns)
df = pd.DataFrame(rows, columns=[
    "ID", "Name", "Source", "Category", "Size", "Upload Date"
])

# Sidebar filter
st.sidebar.header("Filter Datasets")
category_filter = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

# Filtered data
filtered_df = df[df["Category"].isin(category_filter)]

# Metrics
st.metric("Total Datasets", len(df))
st.metric("Filtered Datasets", len(filtered_df))

# Chart
if not filtered_df.empty:
    st.subheader("Dataset Categories")
    st.bar_chart(filtered_df['Category'].value_counts())

# Table
st.subheader(" Dataset Records")
st.dataframe(filtered_df, use_container_width=True)