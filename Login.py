import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

DB_PATH = "Data/intelligence_platform.db"


def get_auth_manager() -> AuthManager:
    if "auth_manager" not in st.session_state:
        db = DatabaseManager(DB_PATH)
        db.connect()
        st.session_state["db_manager"] = db
        st.session_state["auth_manager"] = AuthManager(db)
    return st.session_state["auth_manager"]


def register_user():
    auth = get_auth_manager()

    username = st.text_input("Enter a new username", key="reg_username")
    password = st.text_input("Enter a new password", type="password", key="reg_password")
    role = st.selectbox("Role", ["user", "analyst", "admin"], key="reg_role")

    if st.button("Register"):
        if not username or not password:
            st.warning("Username and password are required.")
            return

        success = auth.register_user(username=username, password=password, role=role)

        if success:
            st.success("You are registered successfully!")
        else:
            st.warning("Username already exists.")


def login_user():
    auth = get_auth_manager()

    username = st.text_input("Enter your username", key="login_username")
    password = st.text_input("Enter your password", type="password", key="login_password")

    if st.button("Login"):
        user = auth.login_user(username=username, password=password)

        if user is None:
            st.error("Invalid username or password.")
            return False

        st.session_state.username = user.get_username()
        st.session_state.logged_in = True
        st.session_state.role = user.get_role()

        st.success(f"Welcome, {user.get_username()}!")
        st.rerun()

    return st.session_state.get("logged_in", False)