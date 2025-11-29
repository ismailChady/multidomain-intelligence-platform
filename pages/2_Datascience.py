import streamlit as st
import pandas as pd
from Database.data_management import connect_db, get_all_datasets

#ACCESS CONTROL
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()


st.set_page_config(page_title="Data Science Dashboard", layout="wide")
st.title("Data Science Dashboard")

#LOAD DATA 
conn = connect_db()
rows = get_all_datasets(conn)
conn.close()

df = pd.DataFrame(rows, columns=[
    "ID", "Name", "Source", "Category", "Size", "Upload Date"
])

#SIDEBAR FILTER
st.sidebar.header("Filter Datasets")
category_filter = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[df["Category"].isin(category_filter)]

st.metric("Total Datasets", len(df))
st.metric("Filtered Datasets", len(filtered_df))

if not filtered_df.empty:
    st.subheader("Dataset Categories")
    st.bar_chart(filtered_df['Category'].value_counts())

#TABLE VIEW 
st.subheader("Dataset Records")
st.dataframe(filtered_df, use_container_width=True)

st.divider()
#INSERT DATASET FORM
st.subheader("Upload New Dataset")
with st.form("insert_dataset"):
    name = st.text_input("Dataset Name")
    source = st.text_input("Source (e.g., IT, Cyber)")
    category = st.text_input("Category")
    size = st.number_input("Size (MB)", min_value=0.0)
    uploaded_by = st.text_input("Uploaded By")
    upload_date = st.date_input("Upload Date")
    submit = st.form_submit_button("Submit Dataset")

    if submit:
        try:
            conn = connect_db()
            insert_query = """
                INSERT INTO datasets_metadata (name, source, category, size, uploaded_by, upload_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            conn.execute(insert_query, (name, source, category, size, uploaded_by, str(upload_date)))
            conn.commit()
            st.success("Dataset uploaded successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.experimental_rerun()

#UPDATE DATASET FORM
st.subheader("Update Dataset Category")
with st.form("update_dataset"):
    selected_id = st.selectbox("Select Dataset ID", df["ID"])
    new_category = st.text_input("New Category")
    submit_update = st.form_submit_button("Update Category")

    if submit_update:
        try:
            conn = connect_db()
            conn.execute("UPDATE datasets_metadata SET category = ? WHERE dataset_id = ?", (new_category, selected_id))
            conn.commit()
            st.success(f"Dataset {selected_id} category updated to '{new_category}'.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.experimental_rerun()

#DELETE DATASET FORM
st.subheader("Delete Dataset")
with st.form("delete_dataset"):
    del_id = st.selectbox("Select Dataset to Delete", df["ID"], key="del_id")
    submit_del = st.form_submit_button("Delete Dataset")

    if submit_del:
        try:
            conn = connect_db()
            conn.execute("DELETE FROM datasets_metadata WHERE dataset_id = ?", (del_id,))
            conn.commit()
            st.warning(f"Dataset {del_id} deleted.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.experimental_rerun()