import sqlite3

DB_PATH = "Data/intelligence_platform.db"

# Connect to DB
def connect_db():
    return sqlite3.connect(DB_PATH)

# USERS 
def get_all_users(conn):
    return conn.execute("SELECT id, username, role FROM users").fetchall()

# CYBER INCIDENTS 
def get_all_incidents(conn):
    return conn.execute("SELECT * FROM cyber_incidents").fetchall()

def insert_incident(conn, title, severity, status, date):
    conn.execute(
        "INSERT INTO cyber_incidents (title, severity, status, date) VALUES (?, ?, ?, ?)",
        (title, severity, status, date)
    )
    conn.commit()

#  IT TICKETS 
def get_all_tickets(conn):
    return conn.execute("SELECT * FROM it_tickets").fetchall()

def insert_ticket(conn, title, priority, status, created_date):
    conn.execute(
        "INSERT INTO it_tickets (title, priority, status, created_date) VALUES (?, ?, ?, ?)",
        (title, priority, status, created_date)
    )
    conn.commit()

# DATASET METADATA 
def get_all_datasets(conn):
    return conn.execute("SELECT * FROM datasets_metadata").fetchall()

def insert_dataset(conn, name, source, category, size):
    conn.execute(
        "INSERT INTO datasets_metadata (name, source, category, size) VALUES (?, ?, ?, ?)",
        (name, source, category, size)
    )
    conn.commit()