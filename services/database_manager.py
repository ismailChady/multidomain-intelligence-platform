import sqlite3
from typing import Any, Iterable, Optional, List, Tuple


class DatabaseManager:
    """Handles SQLite database connections and queries."""

    def __init__(self, db_path: str):
        self._db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None

    # CONNECTION HANDLING
    def connect(self) -> None:
        if self._connection is None:
            # IMPORTANT: allow reuse across threads (Streamlit reruns)
            self._connection = sqlite3.connect(
                self._db_path,
                check_same_thread=False
            )

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    # WRITE QUERY
    def execute_query(self, sql: str, params: Iterable[Any] = ()):
        """
        Execute INSERT, UPDATE, DELETE SQL queries.
        Returns cursor for access if needed.
        """
        if self._connection is None:
            self.connect()

        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        self._connection.commit()
        return cur

    # READ (ONE ROW)
    def fetch_one(self, sql: str, params: Iterable[Any] = ()) -> Optional[Tuple]:
        if self._connection is None:
            self.connect()

        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchone()

    # READ (MULTIPLE ROWS)
    def fetch_all(self, sql: str, params: Iterable[Any] = ()) -> List[Tuple]:
        if self._connection is None:
            self.connect()

        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchall()