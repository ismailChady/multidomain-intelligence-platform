import streamlit as st
import pandas as pd
from Database.data_management import connect_db, get_all_datasets

# ACCESS CONTROL
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()

st.set_page_config(page_title="Data Science Dashboard", layout="wide")
st.title("Data Science Dashboard")

# LOAD DATA
conn = connect_db()
rows = get_all_datasets(conn)
conn.close()


df = pd.DataFrame(rows, columns=[
    "ID", "Name", "Rows", "Columns", "Uploaded By", "Upload Date"
])

# SIDEBAR FILTER 
st.sidebar.header("Filter Datasets")
uploader_filter = st.sidebar.multiselect(
    "Select Uploader",
    df["Uploaded By"].unique(),
    default=list(df["Uploaded By"].unique())
)

filtered_df = df[df["Uploaded By"].isin(uploader_filter)] if uploader_filter else df

# METRICS
col1, col2 = st.columns(2)
col1.metric("Total Datasets", len(df))
col2.metric("Filtered Datasets", len(filtered_df))

# CHART
if not filtered_df.empty:
    st.subheader("Datasets by Uploader")
    st.bar_chart(filtered_df["Uploaded By"].value_counts())

# TABLE VIEW
st.subheader("Dataset Records")
st.dataframe(filtered_df, use_container_width=True)

st.divider()

# INSERT DATASET FORM
st.subheader("Upload New Dataset")
with st.form("insert_dataset"):
    name = st.text_input("Dataset Name")
    rows_val = st.number_input("Rows", min_value=0, step=1)
    cols_val = st.number_input("Columns", min_value=0, step=1)
    uploaded_by = st.text_input("Uploaded By")
    upload_date = st.date_input("Upload Date")
    submit = st.form_submit_button("Submit Dataset")

    if submit:
        try:
            conn = connect_db()
            insert_query = """
                INSERT INTO datasets_metadata (name, rows, columns, uploaded_by, upload_date)
                VALUES (?, ?, ?, ?, ?)
            """
            conn.execute(insert_query, (name, int(rows_val), int(cols_val), uploaded_by, str(upload_date)))
            conn.commit()
            st.success("Dataset uploaded successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.experimental_rerun()

# UPDATE DATASET FORM 
st.subheader("Update Dataset Details")
with st.form("update_dataset"):
    selected_id = st.selectbox("Select Dataset ID", df["ID"])
    new_rows = st.number_input("New Row Count", min_value=0, step=1)
    new_cols = st.number_input("New Column Count", min_value=0, step=1)
    submit_update = st.form_submit_button("Update Dataset")

    if submit_update:
        try:
            conn = connect_db()
            conn.execute(
                "UPDATE datasets_metadata SET rows = ?, columns = ? WHERE dataset_id = ?",
                (int(new_rows), int(new_cols), int(selected_id)),
            )
            conn.commit()
            st.success(f"Dataset {selected_id} updated.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.experimental_rerun()

# DELETE DATASET FORM
st.subheader("Delete Dataset")
with st.form("delete_dataset"):
    del_id = st.selectbox("Select Dataset to Delete", df["ID"], key="del_id")
    submit_del = st.form_submit_button("Delete Dataset")

    if submit_del:
        try:
            conn = connect_db()
            conn.execute("DELETE FROM datasets_metadata WHERE dataset_id = ?", (int(del_id),))
            conn.commit()
            st.warning(f"Dataset {del_id} deleted.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.experimental_rerun()