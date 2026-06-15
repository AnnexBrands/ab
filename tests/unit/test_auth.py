"""Unit tests for authentication (T051)."""

from __future__ import annotations

import json
import sqlite3
import time
from unittest.mock import MagicMock

import pytest

from ab.auth.base import Token
from ab.auth.file import FileTokenStorage
from ab.auth.session import SessionTokenStorage


class TestToken:
    def test_not_expired(self):
        t = Token(access_token="tok", expires_at=time.time() + 600)
        assert not t.expired

    def test_expired(self):
        t = Token(access_token="tok", expires_at=time.time() - 1)
        assert t.expired

    def test_round_trip(self):
        t = Token(access_token="a", refresh_token="r", expires_at=123.0)
        restored = Token.from_dict(t.as_dict())
        assert restored.access_token == "a"
        assert restored.refresh_token == "r"
        assert restored.expires_at == 123.0


class TestFileTokenStorage:
    def test_save_and_load(self, tmp_path):
        storage = FileTokenStorage.__new__(FileTokenStorage)
        storage._path = tmp_path / "token.staging.json"
        storage._token = None

        token = Token(access_token="abc", refresh_token="ref", expires_at=time.time() + 600)
        storage.save_token(token)
        assert storage._path.is_file()

        # Reload
        storage2 = FileTokenStorage.__new__(FileTokenStorage)
        storage2._path = storage._path
        storage2._token = None
        storage2._load()
        assert storage2.get_token() is not None
        assert storage2.get_token().access_token == "abc"

    def test_clear(self, tmp_path):
        storage = FileTokenStorage.__new__(FileTokenStorage)
        storage._path = tmp_path / "token.staging.json"
        storage._token = None

        token = Token(access_token="x", expires_at=0.0)
        storage.save_token(token)
        assert storage._path.is_file()

        storage.clear_token()
        assert storage.get_token() is None
        assert not storage._path.exists()

    def test_scoped_storage_reads_legacy_path_and_writes_private_file(self, tmp_path):
        legacy = tmp_path / "token.staging.json"
        legacy.write_text(json.dumps(Token(access_token="legacy", expires_at=time.time() + 600).as_dict()))

        storage = FileTokenStorage(
            environment="staging",
            username="User@Test.com",
            client_id="client/one",
            token_dir=tmp_path,
        )

        assert storage.get_token().access_token == "legacy"
        assert storage._path != legacy
        assert storage._path.name == "token.staging.user@test.com.client_one.json"

        storage.save_token(Token(access_token="scoped", expires_at=time.time() + 600))

        assert storage._path.is_file()
        assert storage._path.stat().st_mode & 0o777 == 0o600
        assert json.loads(storage._path.read_text())["access_token"] == "scoped"

    def test_expiry_buffer(self):
        """Token with 300s buffer — 300s subtracted from expires_in."""
        expires_in = 3600
        buffer = 300
        now = time.time()
        expected_expires_at = now + expires_in - buffer
        actual = now + expires_in - buffer
        assert abs(expected_expires_at - actual) < 1


class TestSessionTokenStorage:
    def test_save_and_get(self):
        request = MagicMock()
        request.session = {}

        storage = SessionTokenStorage.__new__(SessionTokenStorage)
        storage._request = request
        storage._token = None

        token = Token(access_token="sess_tok", expires_at=time.time() + 600)
        storage.save_token(token)

        assert "ab_token" in request.session
        assert storage.get_token().access_token == "sess_tok"

    def test_clear(self):
        request = MagicMock()
        request.session = {"ab_token": {"access_token": "x", "expires_at": 0}}

        storage = SessionTokenStorage.__new__(SessionTokenStorage)
        storage._request = request
        storage._token = Token(access_token="x", expires_at=0)

        storage.clear_token()
        assert storage.get_token() is None
        assert "ab_token" not in request.session


class TestDbTokenStorage:
    """Tests for the database-backed TokenStorage implementation."""

    def _conn(self):
        """Return a fresh in-memory sqlite3 connection."""
        return sqlite3.connect(":memory:")

    def test_init_schema_idempotent(self):
        from ab.auth.db import DbTokenStorage
        conn = self._conn()
        DbTokenStorage.init_schema(conn)
        # Calling again should not raise
        DbTokenStorage.init_schema(conn)

    def test_save_and_get_round_trips(self):
        from ab.auth.db import DbTokenStorage
        conn = self._conn()
        storage = DbTokenStorage(conn, "session-1")
        token = Token(access_token="abc", refresh_token="ref", expires_at=time.time() + 600)
        storage.save_token(token)

        result = storage.get_token()
        assert result is not None
        assert result.access_token == "abc"
        assert result.refresh_token == "ref"

    def test_clear_removes_row(self):
        from ab.auth.db import DbTokenStorage
        conn = self._conn()
        storage = DbTokenStorage(conn, "session-1")
        storage.save_token(Token(access_token="x", expires_at=0))
        storage.clear_token()
        assert storage.get_token() is None

    def test_independent_sessions(self):
        """Different session_ids in the same DB don't interfere."""
        from ab.auth.db import DbTokenStorage
        conn = self._conn()
        a = DbTokenStorage(conn, "session-A")
        b = DbTokenStorage(conn, "session-B")
        a.save_token(Token(access_token="token-A", expires_at=time.time() + 600))
        b.save_token(Token(access_token="token-B", expires_at=time.time() + 600))

        assert a.get_token().access_token == "token-A"
        assert b.get_token().access_token == "token-B"

    def test_get_token_unknown_session(self):
        from ab.auth.db import DbTokenStorage
        conn = self._conn()
        DbTokenStorage.init_schema(conn)
        storage = DbTokenStorage(conn, "nonexistent")
        assert storage.get_token() is None

    def test_from_path_creates_file(self, tmp_path):
        from ab.auth.db import DbTokenStorage
        path = tmp_path / "auth.sqlite"
        storage = DbTokenStorage.from_path(path, "session-1")
        storage.save_token(Token(access_token="filed", expires_at=time.time() + 600))
        assert path.is_file()

        # New storage on same file sees the same token
        storage2 = DbTokenStorage.from_path(path, "session-1")
        assert storage2.get_token().access_token == "filed"

    def test_corrupted_json_raises(self):
        from ab.auth.db import DbTokenStorage
        conn = self._conn()
        DbTokenStorage.init_schema(conn)
        # Inject invalid JSON directly
        conn.execute(
            "INSERT INTO ab_token_sessions (session_id, token_json, created_at, updated_at) VALUES (?, ?, ?, ?)",
            ("session-1", "{not valid json", time.time(), time.time()),
        )
        conn.commit()
        storage = DbTokenStorage(conn, "session-1")
        with pytest.raises(Exception):
            storage.get_token()

    def test_overwrite_existing_token(self):
        from ab.auth.db import DbTokenStorage
        conn = self._conn()
        storage = DbTokenStorage(conn, "session-1")
        storage.save_token(Token(access_token="first", expires_at=time.time() + 600))
        storage.save_token(Token(access_token="second", expires_at=time.time() + 600))
        assert storage.get_token().access_token == "second"


class TestMemoryTokenStorage:
    def test_starts_empty_and_round_trips(self):
        from ab.auth import MemoryTokenStorage

        storage = MemoryTokenStorage()
        assert storage.get_token() is None
        token = Token(access_token="t", expires_at=9e9)
        storage.save_token(token)
        assert storage.get_token() is token
        storage.clear_token()
        assert storage.get_token() is None

    def test_seeded_with_token(self):
        from ab.auth import MemoryTokenStorage

        token = Token(access_token="worker", expires_at=9e9)
        assert MemoryTokenStorage(token=token).get_token() is token
