import streamlit as st
import pandas as pd
from Database.data_management import connect_db, get_all_tickets

#ACCESS CONTROL
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()

#PAGE CONFIG
st.set_page_config(page_title="IT Operations Dashboard", layout="wide")
st.title("IT Operations Dashboard")

#LOAD DATA
conn = connect_db()
rows = get_all_tickets(conn)
conn.close()

df = pd.DataFrame(rows, columns=[
    "Ticket ID", "Priority", "Description", "Status", "Assigned To", "Created At", "Resolution Time"
])

#SIDEBAR FILTERS
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

filtered_df = df[
    df["Status"].isin(status_filter) & df["Priority"].isin(priority_filter)
]

st.metric("Total Tickets", len(df))
st.metric("Filtered Tickets", len(filtered_df))

if not filtered_df.empty:
    st.subheader(" Ticket Priorities")
    st.bar_chart(filtered_df['Priority'].value_counts())

st.subheader("Ticket Records")
st.dataframe(filtered_df, use_container_width=True)

st.divider()


#INSERT FORM

st.subheader("Add New Ticket")

with st.form("insert_ticket"):
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
    description = st.text_area("Description")
    status = st.selectbox("Status", ["Open", "Assigned", "Resolved"])
    assigned_to = st.text_input("Assigned To")
    created_at = st.date_input("Created Date")
    resolution_time = st.number_input("Resolution Time (hrs)", min_value=0.0)
    submit = st.form_submit_button("Submit Ticket")

    if submit:
        try:
            conn = connect_db()
            insert_query = """
                INSERT INTO it_tickets (priority, description, status, assigned_to, created_at, resolution_time_hours)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            conn.execute(insert_query, (priority, description, status, assigned_to, str(created_at), resolution_time))
            conn.commit()
            st.success("Ticket submitted successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.experimental_rerun()

#UPDATE FORM

st.subheader("Update Ticket Status")

with st.form("update_ticket"):
    selected_id = st.selectbox("Select Ticket ID", df["Ticket ID"])
    new_status = st.selectbox("New Status", ["Open", "Assigned", "Resolved"])
    submit_update = st.form_submit_button("Update Status")

    if submit_update:
        try:
            conn = connect_db()
            conn.execute("UPDATE it_tickets SET status = ? WHERE ticket_id = ?", (new_status, selected_id))
            conn.commit()
            st.success(f"Ticket {selected_id} status updated to '{new_status}'.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.experimental_rerun()

#DELETE FORM

st.subheader("Delete Ticket")

with st.form("delete_ticket"):
    del_id = st.selectbox("Select Ticket to Delete", df["Ticket ID"], key="del_id")
    submit_del = st.form_submit_button("Delete Ticket")

    if submit_del:
        try:
            conn = connect_db()
            conn.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (del_id,))
            conn.commit()
            st.warning(f"Ticket {del_id} deleted.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.experimental_rerun()