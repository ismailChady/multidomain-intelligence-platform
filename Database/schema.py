import sqlite3

DB_PATH = "../Data/intelligence_platform.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    # Cyber Incidents Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id INTEGER PRIMARY KEY,
            timestamp TEXT,
            severity TEXT,
            category TEXT,
            status TEXT,
            description TEXT
        )
    """)

    # IT Tickets Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            ticket_id INTEGER PRIMARY KEY,
            priority TEXT,
            description TEXT,
            status TEXT,
            assigned_to TEXT,
            created_at TEXT,
            resolution_time_hours REAL
        )
    """)

    # Datasets Metadata Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            dataset_id INTEGER PRIMARY KEY,
            name TEXT,
            rows INTEGER,
            columns INTEGER,
            uploaded_by TEXT,
            upload_date TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("All tables created successfully.")

if __name__ == "__main__":
    create_tables()
