import streamlit as st
import pandas as pd
import sqlite3

from services.database_manager import DatabaseManager

DB_PATH = "Data/intelligence_platform.db"


def load_csv_to_db(uploaded_file):
    if uploaded_file is None:
        st.warning("Please upload a CSV file.")
        return

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        return

    # show preview
    st.subheader("CSV Preview")
    st.dataframe(df.head())

    # insert
    try:
        db = DatabaseManager(DB_PATH)
        db.connect()

        # assuming table already exists, and column names match CSV
        rows = df.to_records(index=False)

        insert_query = f"""
        INSERT INTO datasets ({", ".join(df.columns)})
        VALUES ({", ".join(["?" for _ in df.columns])})
        """

        for row in rows:
            db.execute_query(insert_query, row)

        st.success("CSV successfully imported to the database.")

    except sqlite3.Error as e:
        st.error(f"SQLite Error: {e}")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        db.close()