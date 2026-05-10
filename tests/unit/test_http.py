"""Unit tests for HttpClient (T052)."""

from __future__ import annotations

import os
import time
from unittest.mock import MagicMock, patch

import pytest

from ab.auth.base import Token, TokenStorage
from ab.config import ABConnectSettings
from ab.exceptions import AuthenticationError, RequestError
from ab.http import HttpClient


class _StubTokenStorage(TokenStorage):
    def __init__(self):
        self._token = Token(access_token="test_token", expires_at=time.time() + 3600)

    def get_token(self):
        return self._token

    def save_token(self, token):
        self._token = token

    def clear_token(self):
        self._token = None


class _ExpiredRefreshStorage(TokenStorage):
    def __init__(self):
        self._token = Token(access_token="old", refresh_token="refresh", expires_at=time.time() - 1)
        self.cleared = False

    def get_token(self):
        return self._token

    def save_token(self, token):
        self._token = token

    def clear_token(self):
        self.cleared = True
        self._token = None


def _make_client(base_url: str = "https://example.com/api") -> HttpClient:
    env = {
        "ABCONNECT_USERNAME": "u",
        "ABCONNECT_PASSWORD": "p",
        "ABCONNECT_CLIENT_ID": "c",
        "ABCONNECT_CLIENT_SECRET": "s",
    }
    with patch.dict(os.environ, env, clear=False):
        settings = ABConnectSettings()
    return HttpClient(base_url, settings, _StubTokenStorage())


class TestHttpClient:
    def test_bearer_header_injection(self):
        client = _make_client()
        with patch.object(client._session, "request") as mock_req:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.headers = {"Content-Type": "application/json"}
            mock_resp.json.return_value = {"ok": True}
            mock_req.return_value = mock_resp

            client.request("GET", "/test")

            call_kwargs = mock_req.call_args
            assert "Authorization" in call_kwargs.kwargs["headers"]
            assert call_kwargs.kwargs["headers"]["Authorization"] == "Bearer test_token"

    def test_base_url_routing(self):
        client = _make_client("https://portal.staging.abconnect.co/api/api")
        with patch.object(client._session, "request") as mock_req:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.headers = {"Content-Type": "application/json"}
            mock_resp.json.return_value = {}
            mock_req.return_value = mock_resp

            client.request("GET", "/companies/123")

            url = mock_req.call_args.kwargs["url"]
            assert url == "https://portal.staging.abconnect.co/api/api/companies/123"

    def test_timeout_passed(self):
        client = _make_client()
        with patch.object(client._session, "request") as mock_req:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.headers = {"Content-Type": "application/json"}
            mock_resp.json.return_value = {}
            mock_req.return_value = mock_resp

            client.request("GET", "/test")

            assert mock_req.call_args.kwargs["timeout"] == 30

    def test_retry_on_503(self):
        client = _make_client()
        with patch.object(client._session, "request") as mock_req, \
             patch("ab.http.time.sleep"):  # skip actual sleep
            fail_resp = MagicMock()
            fail_resp.status_code = 503

            ok_resp = MagicMock()
            ok_resp.status_code = 200
            ok_resp.headers = {"Content-Type": "application/json"}
            ok_resp.json.return_value = {"ok": True}

            mock_req.side_effect = [fail_resp, ok_resp]

            result = client.request("GET", "/test")
            assert result == {"ok": True}
            assert mock_req.call_count == 2

    def test_raises_request_error_on_4xx(self):
        client = _make_client()
        with patch.object(client._session, "request") as mock_req:
            mock_resp = MagicMock()
            mock_resp.status_code = 404
            mock_resp.text = "Not found"
            mock_resp.json.side_effect = Exception("no json")
            mock_resp.headers = {"Content-Type": "text/plain"}
            mock_req.return_value = mock_resp

            with pytest.raises(RequestError) as exc_info:
                client.request("GET", "/missing")
            assert exc_info.value.status_code == 404

    def test_204_returns_none(self):
        client = _make_client()
        with patch.object(client._session, "request") as mock_req:
            mock_resp = MagicMock()
            mock_resp.status_code = 204
            mock_resp.headers = {}
            mock_req.return_value = mock_resp

            result = client.request("DELETE", "/resource/1")
            assert result is None

    def test_expired_refresh_without_password_fallback_raises(self):
        env = {
            "ABCONNECT_CLIENT_ID": "c",
            "ABCONNECT_CLIENT_SECRET": "s",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = ABConnectSettings(require_credentials=False)
        storage = _ExpiredRefreshStorage()
        client = HttpClient(
            "https://example.com/api",
            settings,
            storage,
            allow_password_fallback=False,
        )
        with patch("ab.http.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.ok = False
            mock_resp.status_code = 400
            mock_resp.text = "bad refresh"
            mock_post.return_value = mock_resp

            with pytest.raises(AuthenticationError, match="No valid ABConnect token"):
                client.request("GET", "/test")

        assert storage.cleared is True

    def test_password_grant_with_uses_explicit_credentials(self):
        client = _make_client()
        with patch("ab.http.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.ok = True
            mock_resp.json.return_value = {
                "access_token": "new-token",
                "refresh_token": "new-refresh",
                "expires_in": 3600,
                "token_type": "Bearer",
            }
            mock_post.return_value = mock_resp

            token = client._password_grant_with(username="form-user", password="form-pass")

        assert token.access_token == "new-token"
        assert mock_post.call_args.kwargs["data"]["username"] == "form-user"
        assert mock_post.call_args.kwargs["data"]["password"] == "form-pass"
