import pandas as pd
import sqlite3

# Paths
DB_PATH = "Data/intelligence_platform.db"
cyber_path = "Data/cyber_incidents.csv"
ticket_path = "Data/it_tickets.csv"
ds_path = "Data/datasets_metadata.csv"

# Load data
cyber_df = pd.read_csv(cyber_path)
ticket_df = pd.read_csv(ticket_path)
ds_df = pd.read_csv(ds_path)

# Connect to DB
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Optional: clear existing rows
cursor.execute("DELETE FROM cyber_incidents")
cursor.execute("DELETE FROM it_tickets")
cursor.execute("DELETE FROM datasets_metadata")

# Insert
cyber_df.to_sql("cyber_incidents", conn, if_exists="append", index=False)
ticket_df.to_sql("it_tickets", conn, if_exists="append", index=False)
ds_df.to_sql("datasets_metadata", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("CSV data imported successfully.")