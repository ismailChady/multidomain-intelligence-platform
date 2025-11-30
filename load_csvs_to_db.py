import sqlite3
import pandas as pd
from pathlib import Path

# Base directory = folder where THIS file lives (ProjectFolder)
BASE_DIR = Path(__file__).resolve().parent

# Path to the SQLite database
DB_PATH = BASE_DIR / "Data" / "intelligence_platform.db"


def load_table(csv_path: Path, table_name: str):
    try:
        df = pd.read_csv(csv_path)

        with sqlite3.connect(DB_PATH) as conn:
            df.to_sql(table_name, conn, if_exists="append", index=False)

        print(f"[✓] Loaded {len(df)} rows into {table_name}")
    except Exception as e:
        print(f"[✗] Failed to load {table_name}: {e}")


if __name__ == "__main__":
    data_dir = BASE_DIR / "Data"

    # Cybersecurity
    load_table(
        data_dir / "cyber_incidents.csv",
        "cyber_incidents"
    )

    # IT Operations
    load_table(
        data_dir / "it_tickets.csv",
        "it_tickets"
    )

    # Data Science Datasets (uses EXACT same columns as CSV)
    load_table(
        data_dir / "datasets_metadata.csv",
        "datasets_metadata"
    )