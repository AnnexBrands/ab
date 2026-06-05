"""Unit tests for ABConnectAPI authentication construction."""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

from ab import ABConnectAPI
from ab.auth.base import Token, TokenStorage


class _MemoryStorage(TokenStorage):
    def __init__(self):
        self.token = None

    def get_token(self):
        return self.token

    def save_token(self, token):
        self.token = token

    def clear_token(self):
        self.token = None


def test_token_storage_construction_does_not_require_username_password(tmp_path, monkeypatch):
    # Isolate from any developer ``./.env`` at the repo root: load_settings()
    # auto-reads ``./.env`` from the CWD when env/env_file are unset, which
    # would otherwise leak ABCONNECT_USERNAME and break the empty-credential
    # assertion. Running from an empty tmp dir guarantees no ambient .env.
    monkeypatch.chdir(tmp_path)
    env = {
        "ABCONNECT_CLIENT_ID": "cid",
        "ABCONNECT_CLIENT_SECRET": "secret",
    }
    with patch.dict(os.environ, env, clear=True):
        api = ABConnectAPI(token_storage=_MemoryStorage())

    assert api._settings.username == ""
    assert api._settings.password == ""


def test_allow_password_fallback_flag_is_applied_to_clients():
    env = {
        "ABCONNECT_CLIENT_ID": "cid",
        "ABCONNECT_CLIENT_SECRET": "secret",
    }
    with patch.dict(os.environ, env, clear=True):
        api = ABConnectAPI(token_storage=_MemoryStorage(), allow_password_fallback=False)

    assert api._acportal._allow_password_fallback is False
    assert api._catalog._allow_password_fallback is False
    assert api._abc._allow_password_fallback is False


def test_login_primes_selected_token_storage():
    env = {
        "ABCONNECT_CLIENT_ID": "cid",
        "ABCONNECT_CLIENT_SECRET": "secret",
    }
    storage = _MemoryStorage()
    with patch.dict(os.environ, env, clear=True):
        api = ABConnectAPI(token_storage=storage)

    with patch("ab.http.requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {
            "access_token": "access",
            "refresh_token": "refresh",
            "expires_in": 3600,
            "token_type": "Bearer",
        }
        mock_post.return_value = mock_resp

        token = api.login("user@example.com", "secret")

    assert isinstance(token, Token)
    assert storage.token is token
    assert mock_post.call_args.kwargs["data"]["username"] == "user@example.com"
