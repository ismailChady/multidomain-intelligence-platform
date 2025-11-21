import streamlit as st
import pandas as pd
from Database.data_management import connect_db, get_all_datasets

# Session check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()

# Page config
st.set_page_config(page_title="Datascience Dashboard", layout="wide")
st.title("Datascience Dashboard")

# Sidebar filters
st.sidebar.header("Filter Datasets")
category_filter = st.sidebar.multiselect(
    "Select Category",
    ["AI", "ML", "IoT", "Healthcare", "Security"],
    default=["AI", "ML", "IoT", "Healthcare", "Security"]
)

source_filter = st.sidebar.multiselect(
    "Select Source",
    ["Kaggle", "UCI", "Internal", "External"],
    default=["Kaggle", "UCI", "Internal", "External"]
)

# Load data
conn = connect_db()
rows = get_all_datasets(conn)
conn.close()

# Convert to DataFrame
df = pd.DataFrame(rows, columns=["ID", "Name", "Source", "Category", "Size"])

# Apply filters
filtered_df = df[
    df["Category"].isin(category_filter) &
    df["Source"].isin(source_filter)
]

# Metrics
st.metric("Total Datasets", len(df))
st.metric("Filtered", len(filtered_df))

# Show chart (optional)
if not filtered_df.empty:
    st.subheader("Datasets by Category")
    cat_chart = filtered_df.groupby("Category").size().reset_index(name="Count")
    st.bar_chart(cat_chart.set_index("Category"))

# Show table
st.subheader("Filtered Datasets")
st.dataframe(filtered_df)