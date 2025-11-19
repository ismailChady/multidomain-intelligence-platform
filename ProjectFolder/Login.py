import bcrypt 
import os      
import csv     
import streamlit as st  

# File path for user data
USER_FILE = "Data/users.csv"

# Function to register a new user
def register_user():
    # Get user input
    username = st.text_input("Enter a new username", key="reg_username")
    password = st.text_input("Enter a new password", type="password", key="reg_password")

    
    if st.button("Register"):
        if not username or not password:
            st.warning("Username and password are required.")
            return

        # If file doesn't exist, create it with header
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'password'])

        # Check if username already exists
        with open(USER_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    st.warning("Username already exists.")
                    return

        # Hash the password and save new user
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        with open(USER_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([username, hashed.decode()])
        st.success("You are registered successfully!")

# Function to login an existing user
def login_user():
    # Get user input
    username = st.text_input("Enter your username", key="login_username")
    password = st.text_input("Enter your password", type="password", key="login_password")

    # If Login button is clicked
    if st.button("Login"):
        # Check if the user file exists
        if not os.path.exists(USER_FILE):
            st.error("No users found. Please register first.")
            return False

        # Read the user data and verify credentials
        with open(USER_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    # Verify the password using bcrypt
                    if bcrypt.checkpw(password.encode(), row['password'].encode()):
                        st.session_state.username = username
                        st.session_state.logged_in = True
                        return True
                    else:
                        st.error("Incorrect password.")
                        return False
        # If username not found
        st.error("Username not found.")
        return False

    # Return False if login button is not clicked
    return False