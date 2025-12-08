import streamlit as st
import pandas as pd
from Database.data_management import connect_db, get_all_datasets
from google import genai
from models.dataset import Dataset

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

datasets = [
    Dataset(
        dataset_id=row[0],
        name=row[1],
        rows=row[2],
        columns=row[3],
        uploaded_by=row[4],
        upload_date=row[5],
    )
    for row in rows
]

df = pd.DataFrame([d.to_dict() for d in datasets])

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

# AI DATA ANALYST SECTION 

st.divider()
st.subheader("📊 AI Data Analyst")

st.write(
    "Use this assistant to analyse the datasets currently shown above. "
    "You can ask about dataset sizes, who uploads the most, or what to clean up or document."
)

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash"

ds_question = st.text_area(
    "Ask a question about these datasets:",
    placeholder="e.g. Which datasets look the largest or most important? What should I document or archive?",
    key="ds_ai_question",
)

if st.button("Ask AI (Data Science)", key="ds_ai_button"):
    if filtered_df.empty:
        st.warning("There are no datasets in the current filtered view. Try changing the filters first.")
    elif not ds_question.strip():
        st.warning("Please type a question before asking the AI.")
    else:
        with st.spinner("AI reviewing your datasets..."):
            context_csv = filtered_df.to_csv(index=False)

            prompt = f"""
You are acting as a data analyst helping manage a catalogue of datasets.

The CSV below contains the datasets currently visible in the dashboard.
Columns may include: ID, Name, Rows, Columns, Uploaded By, Upload Date.

1. Briefly summarise what you notice (e.g., which datasets are largest, who uploads most, any patterns).
2. Answer the user's question directly, using this data where possible.
3. Suggest 3–5 practical recommendations about storage, documentation, quality checks, or archiving.

DATASET CATALOGUE (CSV):

{context_csv}

USER QUESTION: {ds_question}
"""

            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI error: {e}")

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
            conn.execute(
                insert_query,
                (name, int(rows_val), int(cols_val), uploaded_by, str(upload_date))
            )
            conn.commit()
            st.success("Dataset uploaded successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.rerun()

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
            st.rerun()

# DELETE DATASET FORM
st.subheader("Delete Dataset")
with st.form("delete_dataset"):
    del_id = st.selectbox("Select Dataset to Delete", df["ID"], key="del_id")
    submit_del = st.form_submit_button("Delete Dataset")

    if submit_del:
        try:
            conn = connect_db()
            conn.execute(
                "DELETE FROM datasets_metadata WHERE dataset_id = ?",
                (int(del_id),)
            )
            conn.commit()
            st.warning(f"Dataset {del_id} deleted.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
            st.rerun()