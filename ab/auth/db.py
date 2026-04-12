"""Database-backed token storage.

Persists tokens in a database (default: SQLite) keyed by an opaque session ID.
Suitable for multi-user web applications where each user has their own session.

The schema is a single table; tokens are stored as JSON blobs of
``Token.as_dict()``. The default constructor accepts any DB-API 2.0
connection; the :meth:`from_path` convenience opens a SQLite file.
"""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Optional, Union

from ab.auth.base import Token, TokenStorage

_TABLE = "ab_token_sessions"
_SCHEMA = f"""
CREATE TABLE IF NOT EXISTS {_TABLE} (
    session_id TEXT PRIMARY KEY,
    token_json TEXT NOT NULL,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
)
"""


class DbTokenStorage(TokenStorage):
    """Stores tokens in a database, keyed by session ID.

    Args:
        connection: A DB-API 2.0 connection (e.g., :class:`sqlite3.Connection`).
            Caller is responsible for the connection lifecycle.
        session_id: The opaque session identifier this storage instance manages.
            Multiple instances with different session IDs can share the same
            connection without interference.

    The schema is created automatically on first instantiation. Use
    :meth:`from_path` to open a SQLite file directly.
    """

    def __init__(self, connection: Any, session_id: str) -> None:
        self._conn = connection
        self._session_id = session_id
        self.init_schema(connection)

    @classmethod
    def from_path(cls, path: Union[str, Path], session_id: str) -> "DbTokenStorage":
        """Open a SQLite database at *path* and return a storage instance."""
        conn = sqlite3.connect(str(path))
        return cls(conn, session_id)

    @staticmethod
    def init_schema(connection: Any) -> None:
        """Create the token table if it does not exist (idempotent)."""
        cur = connection.cursor()
        cur.execute(_SCHEMA)
        connection.commit()

    def get_token(self) -> Optional[Token]:
        cur = self._conn.cursor()
        cur.execute(
            f"SELECT token_json FROM {_TABLE} WHERE session_id = ?",
            (self._session_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        # Deserialization failure raises explicitly (per spec FR-005)
        data = json.loads(row[0])
        return Token.from_dict(data)

    def save_token(self, token: Token) -> None:
        now = time.time()
        token_json = json.dumps(token.as_dict())
        cur = self._conn.cursor()
        cur.execute(
            f"""INSERT INTO {_TABLE} (session_id, token_json, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    token_json = excluded.token_json,
                    updated_at = excluded.updated_at""",
            (self._session_id, token_json, now, now),
        )
        self._conn.commit()

    def clear_token(self) -> None:
        cur = self._conn.cursor()
        cur.execute(
            f"DELETE FROM {_TABLE} WHERE session_id = ?",
            (self._session_id,),
        )
        self._conn.commit()
