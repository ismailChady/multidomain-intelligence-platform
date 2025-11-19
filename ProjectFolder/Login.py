import bcrypt
import os
import csv
import streamlit as st

USER_FILE = "Data/users.csv"

def register_user():
    username = st.text_input("Enter a new username", key="reg_username")
    password = st.text_input("Enter a new password", type="password", key="reg_password")

    if st.button("Register"):
        if not username or not password:
            st.warning("Username and password are required.")
            return

        if not os.path.exists(USER_FILE):
            with open(USER_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'password'])

        with open(USER_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    st.warning("Username already exists.")
                    return

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        with open(USER_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([username, hashed.decode()])
        st.success("You are registered successfully!")

def login_user():
    username = st.text_input("Enter your username", key="login_username")
    password = st.text_input("Enter your password", type="password", key="login_password")

    if st.button("Login"):
        if not os.path.exists(USER_FILE):
            st.error("No users found. Please register first.")
            return False

        with open(USER_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    if bcrypt.checkpw(password.encode(), row['password'].encode()):
                        st.session_state.username = username
                        return True
                    else:
                        st.error("Incorrect password.")
                        return False
        st.error("Username not found.")
        return False