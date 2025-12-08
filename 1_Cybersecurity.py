import streamlit as st
import pandas as pd

from services.database_manager import DatabaseManager
from services.ai_assistant import AIAssistant
from models.security_incident import SecurityIncident

DB_PATH = "Data/intelligence_platform.db"


# ---------- SERVICE GETTERS ----------

def get_db() -> DatabaseManager:
    """
    Return a shared DatabaseManager instance stored in session_state.

    DatabaseManager itself opens and closes SQLite connections inside its
    own methods (execute_query, fetch_all, fetch_one), so we do NOT call
    db.connect() here.
    """
    if "db_manager" not in st.session_state:
        st.session_state["db_manager"] = DatabaseManager(DB_PATH)
    return st.session_state["db_manager"]


def get_ai_assistant() -> AIAssistant:
    """Return a shared AIAssistant instance stored in session_state."""
    if "ai_assistant" not in st.session_state:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.session_state["ai_assistant"] = AIAssistant(api_key=api_key)
    return st.session_state["ai_assistant"]


# ---------- DATA LOADING & TRANSFORM ----------

def load_incidents(db: DatabaseManager) -> list[SecurityIncident]:
    """Load incidents from DB and wrap into SecurityIncident objects."""
    rows = db.fetch_all(
        """
        SELECT incident_id, timestamp, severity, category, status, description
        FROM cyber_incidents
        ORDER BY timestamp DESC
        """
    )

    incidents: list[SecurityIncident] = []
    for row in rows:
        incident = SecurityIncident(
            incident_id=row[0],
            timestamp=row[1],
            severity=row[2],
            category=row[3],
            status=row[4],
            description=row[5],
        )
        incidents.append(incident)

    return incidents


def incidents_to_dataframe(incidents: list[SecurityIncident]) -> pd.DataFrame:
    """
    Convert a list of SecurityIncident objects into a DataFrame.

    Assumes SecurityIncident.to_dict() returns:
    incident_id, timestamp, severity, category, status, description.
    """
    if not incidents:
        return pd.DataFrame(
            columns=[
                "incident_id", "timestamp",
                "severity", "category",
                "status", "description",
            ]
        )

    return pd.DataFrame([inc.to_dict() for inc in incidents])


# ---------- MAIN PAGE ----------

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to view this page.")
    st.stop()

st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")
st.title("Cybersecurity Incident Dashboard")

st.sidebar.header("Filter Incidents")

status_filter = st.sidebar.multiselect(
    "Select Status",
    ["Open", "Closed", "Resolved", "In Progress", "Investigating"],
    default=["Open", "Closed", "Resolved", "In Progress", "Investigating"],
)

severity_filter = st.sidebar.multiselect(
    "Select Severity",
    ["Low", "Medium", "High", "Critical"],
    default=["Low", "Medium", "High", "Critical"],
)

db = get_db()
incidents = load_incidents(db)
df = incidents_to_dataframe(incidents)

if not df.empty:
    filtered_df = df[
        df["status"].str.lower().isin([s.lower() for s in status_filter])
        & df["severity"].str.lower().isin([s.lower() for s in severity_filter])
    ]
else:
    filtered_df = df

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Incidents", len(df))
with col2:
    st.metric("Filtered Incidents", len(filtered_df))

# uses SecurityIncident.is_high_risk()
high_risk_count = sum(1 for incident in incidents if incident.is_high_risk())
with col3:
    st.metric("High/Critical Incidents", int(high_risk_count))


# ---------- CHARTS ----------

if not filtered_df.empty:
    st.subheader("Incidents Over Time")

    chart_df = filtered_df.copy()
    chart_df["date"] = chart_df["timestamp"].astype(str).str.slice(0, 10)

    daily_counts = (
        chart_df.groupby("date")
        .size()
        .reset_index(name="Incidents")
        .sort_values("date")
        .set_index("date")
    )

    st.line_chart(daily_counts["Incidents"])

if not filtered_df.empty:
    st.subheader("Incidents by Severity")
    st.bar_chart(filtered_df["severity"].value_counts())

st.subheader("Incident Records")
st.dataframe(filtered_df, use_container_width=True)


# ---------- AI SECURITY ANALYST SECTION ----------

st.divider()
st.subheader("🔐 AI Security Analyst")

st.write(
    "Use the assistant to analyse the incidents currently displayed above. "
    "You can ask about trends, risk levels, and which incidents to prioritise."
)

ai = get_ai_assistant()

user_question = st.text_area(
    "Ask a cybersecurity question about these incidents:",
    placeholder="e.g. What are the biggest risks here? Which incidents should I handle first?",
    key="cyber_ai_question",
)

if st.button("Ask AI (Cybersecurity)", key="cyber_ai_button"):
    if filtered_df.empty:
        st.warning("There are no incidents in the current filtered view. Try changing the filters first.")
    elif not user_question.strip():
        st.warning("Please type a question before asking the AI.")
    else:
        with st.spinner("AI analysing your incidents..."):
            context_csv = filtered_df.to_csv(index=False)

            prompt = f"""
You are acting as a cybersecurity analyst reviewing incidents from a dashboard.

The CSV below contains all the incidents currently visible to the user.
Columns may include: incident_id, timestamp, severity, category, status, description.

1. Briefly summarise what you notice in the data (severity mix, status, common categories).
2. Answer the user's question directly, using the data where possible.
3. Give 3–5 clear, practical recommendations for what the user should do next,
   ordered by priority.

INCIDENT DATA (CSV):

{context_csv}

USER QUESTION: {user_question}
"""

            reply = ai.send_message(prompt)
            st.markdown(reply)

st.divider()


# ---------- NEW INCIDENT FORM ----------

st.subheader("Add New Incident")

with st.form("insert_form"):
    timestamp = st.date_input("Incident Date")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    category = st.text_input("Category")
    status = st.selectbox(
        "Status",
        ["Open", "Closed", "Resolved", "In Progress", "Investigating"],
    )
    description = st.text_area("Description")

    submit_insert = st.form_submit_button("Submit Incident")

    if submit_insert:
        try:
            db.execute_query(
                """
                INSERT INTO cyber_incidents (timestamp, severity, category, status, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                (str(timestamp), severity, category, status, description),
            )
            st.success("Incident submitted successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            st.rerun()


# ---------- UPDATE INCIDENT FORM ----------

st.subheader("Update Incident Status")

if df.empty:
    st.info("No incidents available to update.")
else:
    with st.form("update_form"):
        selected_id = st.selectbox("Select Incident ID to Update", df["incident_id"])
        new_status = st.selectbox(
            "New Status",
            ["Open", "Closed", "Resolved", "In Progress", "Investigating"],
        )
        submit_update = st.form_submit_button("Update Status")

        if submit_update:
            try:
                db.execute_query(
                    "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?",
                    (new_status, selected_id),
                )
                st.success(f"Incident {selected_id} status updated to '{new_status}'.")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                st.rerun()


# ---------- DELETE INCIDENT FORM ----------

st.subheader("Delete Incident")

if df.empty:
    st.info("No incidents available to delete.")
else:
    with st.form("delete_form"):
        delete_id = st.selectbox(
            "Select Incident ID to Delete",
            df["incident_id"],
            key="del_id",
        )
        submit_delete = st.form_submit_button("Delete Incident")

        if submit_delete:
            try:
                db.execute_query(
                    "DELETE FROM cyber_incidents WHERE incident_id = ?",
                    (delete_id,),
                )
                st.warning(f"Incident {delete_id} deleted.")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                st.rerun()