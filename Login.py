import bcrypt
import sqlite3
import streamlit as st

# Database path
DB_PATH = "Data/intelligence_platform.db"

#REGISTER USER
def register_user():
    username = st.text_input("Enter a new username", key="reg_username")
    password = st.text_input("Enter a new password", type="password", key="reg_password")

    if st.button("Register"):
        if not username or not password:
            st.warning("Username and password are required.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if username exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            st.warning("Username already exists.")
            conn.close()
            return

        # Hash password
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed.decode()))
        conn.commit()
        conn.close()

        st.success("You are registered successfully!")

#LOGIN USER
def login_user():
    username = st.text_input("Enter your username", key="login_username")
    password = st.text_input("Enter your password", type="password", key="login_password")

    if st.button("Login"):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and bcrypt.checkpw(password.encode(), result[0].encode()):
            st.session_state.username = username
            st.session_state.logged_in = True
            return True
        elif result:
            st.error("Incorrect password.")
        else:
            st.error("Username not found.")
        return False

    return False