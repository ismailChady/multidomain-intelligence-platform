import sqlite3
import hashlib
from typing import Optional

from models.user import User
from services.database_manager import DatabaseManager


class SimpleHasher:
    """Very basic hasher using SHA256 (demo only, not for production)."""

    @staticmethod
    def hash_password(plain: str) -> str:
        return hashlib.sha256(plain.encode("utf-8")).hexdigest()

    @staticmethod
    def check_password(plain: str, hashed: str) -> bool:
        return SimpleHasher.hash_password(plain) == hashed


class AuthManager:
    """Handles user registration and login."""

    def __init__(self, db: DatabaseManager):
        self._db = db

    def register_user(self, username: str, password: str, role: str = "user") -> tuple[bool, str]:
        """
        Register a new user.
        Returns (success: bool, message: str).
        """

        # 1) Check if username already exists
        existing = self._db.fetch_one(
            "SELECT 1 FROM users WHERE username = ?",
            (username,),
        )
        if existing is not None:
            return False, "Username already exists. Please choose another one."

        password_hash = SimpleHasher.hash_password(password)

        try:
            self._db.execute_query(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role),
            )
            return True, "User registered successfully."
        except sqlite3.IntegrityError:
            # Fallback if DB still complains (UNIQUE constraint)
            return False, "Username already exists (database constraint)."
        except Exception as e:
            return False, f"An unexpected error occurred: {e}"

    def login_user(self, username: str, password: str) -> Optional[User]:
        """
        Attempt to log in a user.
        Returns a User object if successful, otherwise None.
        """
        row = self._db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )

        if row is None:
            return None

        username_db, password_hash_db, role_db = row

        if SimpleHasher.check_password(password, password_hash_db):
            return User(username_db, password_hash_db, role_db)

        return None