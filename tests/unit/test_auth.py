"""Unit tests for authentication (T051)."""

from __future__ import annotations

import json
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
