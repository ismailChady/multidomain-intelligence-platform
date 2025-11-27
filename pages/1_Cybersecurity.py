import streamlit as st
import pandas as pd
from Database.data_management import connect_db, get_all_incidents, insert_incident

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
    ["Open", "Closed", "Resolved", "In Progress", "Investigating"],
    default=["Open", "Closed", "Resolved", "In Progress", "Investigating"]
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

# Match the database schema
df = pd.DataFrame(rows, columns=[
    "incident_id", "timestamp", "severity", "category", "status", "description"
])

# Filter
filtered_df = df[
    df["status"].str.lower().isin([s.lower() for s in status_filter]) &
    df["severity"].str.lower().isin([s.lower() for s in severity_filter])
]

# Metrics
st.metric("Total Incidents", len(df))
st.metric("Filtered Incidents", len(filtered_df))

# Charts
if not filtered_df.empty:
    st.subheader("Incidents Over Time")
    chart_df = filtered_df.groupby("timestamp").size().reset_index(name="Incidents")
    st.line_chart(chart_df.rename(columns={"timestamp": "index"}).set_index("index"))

# Table
st.subheader("Incident Records")
st.dataframe(filtered_df, use_container_width=True)

st.divider()

# INSERT FORM
st.subheader("Add New Incident")
with st.form("insert_form"):
    timestamp = st.date_input("Incident Date")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    category = st.text_input("Category")
    status = st.selectbox("Status", ["Open", "Closed", "Resolved", "In Progress", "Investigating"])
    description = st.text_area("Description")
    submit_insert = st.form_submit_button("Submit Incident")

    if submit_insert:
        conn = connect_db()
        insert_query = """
            INSERT INTO cyber_incidents (timestamp, severity, category, status, description)
            VALUES (?, ?, ?, ?, ?)
        """
        conn.execute(insert_query, (str(timestamp), severity, category, status, description))
        conn.commit()
        conn.close()
        st.success("Incident submitted successfully.")
        st.experimental_rerun()

# update form
st.subheader("Update Incident Status")
with st.form("update_form"):
    selected_id = st.selectbox("Select Incident ID to Update", df["incident_id"])
    new_status = st.selectbox("New Status", ["Open", "Closed", "Resolved", "In Progress", "Investigating"])
    submit_update = st.form_submit_button("Update Status")

    if submit_update:
        conn = connect_db()
        update_query = "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?"
        conn.execute(update_query, (new_status, selected_id))
        conn.commit()
        conn.close()
        st.success(f"Incident {selected_id} status updated to '{new_status}'.")
        st.experimental_rerun()

#Delete form
st.subheader("Delete Incident")
with st.form("delete_form"):
    delete_id = st.selectbox("Select Incident ID to Delete", df["incident_id"], key="del_id")
    submit_delete = st.form_submit_button("Delete Incident")

    if submit_delete:
        conn = connect_db()
        delete_query = "DELETE FROM cyber_incidents WHERE incident_id = ?"
        conn.execute(delete_query, (delete_id,))
        conn.commit()
        conn.close()
        st.warning(f"Incident {delete_id} deleted.")
        st.experimental_rerun()