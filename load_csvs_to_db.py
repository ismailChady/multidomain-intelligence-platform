import sqlite3
import pandas as pd

# Path to the SQLite database
DB_PATH = "Data/intelligence_platform.db"

def load_table(csv_path, table_name, drop_columns=None):
    try:
        df = pd.read_csv(csv_path)

        # Optionally drop columns if they don't exist in schema
        if drop_columns:
            df.drop(columns=drop_columns, inplace=True, errors='ignore')

        with sqlite3.connect(DB_PATH) as conn:
            df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"[✓] Loaded {len(df)} rows into {table_name}")
    except Exception as e:
        print(f"[✗] Failed to load {table_name}: {e}")

if __name__ == "__main__":
    # Cybersecurity
    load_table(
        "Data/cyber_incidents.csv",
        "cyber_incidents"
    )

    # IT Operations
    load_table(
        "Data/it_tickets.csv",
        "it_tickets"
    )

    # Data Science Datasets
    load_table(
        "Data/datasets_metadata.csv",
        "datasets_metadata"
    )