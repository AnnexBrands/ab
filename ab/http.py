"""Unified HTTP client for all ABConnect API surfaces.

Wraps :class:`requests.Session` with connection pooling, Bearer JWT
injection, timeout enforcement, and retry with exponential backoff for
transient errors (429, 502, 503).
"""

from __future__ import annotations

import logging
import time
from typing import Any, BinaryIO, Dict, Mapping, Optional, Tuple, Union

import requests

from ab.auth.base import Token, TokenStorage
from ab.config import ABConnectSettings
from ab.exceptions import AuthenticationError, RequestError

logger = logging.getLogger(__name__)

_RETRYABLE_STATUS_CODES = {429, 502, 503}
_TOKEN_EXPIRY_BUFFER = 300  # seconds


class HttpClient:
    """Low-level HTTP transport shared by all endpoint classes.

    A single :class:`HttpClient` is created per API surface (ACPortal,
    Catalog, ABC) and owns a :class:`requests.Session` for connection
    pooling.
    """

    def __init__(
        self,
        base_url: str,
        settings: ABConnectSettings,
        token_storage: TokenStorage,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._settings = settings
        self._token_storage = token_storage
        self._session = requests.Session()

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def _ensure_token(self) -> Token:
        """Return a valid access token, authenticating or refreshing as needed."""
        token = self._token_storage.get_token()

        if token and not token.expired:
            return token

        # Try refresh first
        if token and token.refresh_token:
            refreshed = self._refresh_token(token.refresh_token)
            if refreshed:
                return refreshed

        # Fall back to password grant
        return self._password_grant()

    def _password_grant(self) -> Token:
        data = {
            "grant_type": "password",
            "username": self._settings.username,
            "password": self._settings.password,
            "client_id": self._settings.client_id,
            "client_secret": self._settings.client_secret,
            "scope": "offline_access",
        }
        resp = requests.post(self._settings.identity_url, data=data, timeout=self._settings.timeout)
        if not resp.ok:
            raise AuthenticationError(
                f"Login failed for {self._settings.username}: {resp.status_code} {resp.text}"
            )
        return self._store_token(resp.json())

    def _refresh_token(self, refresh_token: str) -> Optional[Token]:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self._settings.client_id,
            "client_secret": self._settings.client_secret,
        }
        try:
            resp = requests.post(self._settings.identity_url, data=data, timeout=self._settings.timeout)
            if resp.ok:
                return self._store_token(resp.json())
        except Exception:
            logger.info("Refresh token failed, will attempt password grant")
        return None

    def _store_token(self, payload: dict) -> Token:
        token = Token(
            access_token=payload["access_token"],
            refresh_token=payload.get("refresh_token"),
            expires_at=time.time() + payload.get("expires_in", 3600) - _TOKEN_EXPIRY_BUFFER,
            token_type=payload.get("token_type", "Bearer"),
        )
        self._token_storage.save_token(token)
        return token

    # ------------------------------------------------------------------
    # Request helpers
    # ------------------------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        data: Any = None,
        files: Optional[Mapping[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        raw: bool = False,
    ) -> Any:
        """Send an HTTP request with auth, timeout, and retry logic.

        Returns parsed JSON, raw bytes, ``None`` (for 204), or the raw
        :class:`requests.Response` when *raw* is ``True``.
        """
        token = self._ensure_token()
        url = f"{self._base_url}{path}"

        req_headers: Dict[str, str] = {"Authorization": f"Bearer {token.access_token}"}
        if headers:
            req_headers.update(headers)

        last_exc: Optional[Exception] = None

        for attempt in range(1, self._settings.max_retries + 1):
            logger.debug("%s %s (attempt %d)", method.upper(), url, attempt)

            try:
                resp = self._session.request(
                    method=method.upper(),
                    url=url,
                    headers=req_headers,
                    params=params,
                    json=json,
                    data=data,
                    files=files,
                    timeout=self._settings.timeout,
                )
            except requests.RequestException as exc:
                last_exc = exc
                if attempt < self._settings.max_retries:
                    self._backoff(attempt)
                    continue
                raise RequestError(0, str(exc)) from exc

            if resp.status_code in _RETRYABLE_STATUS_CODES and attempt < self._settings.max_retries:
                self._backoff(attempt)
                continue

            if raw:
                return resp

            return self._handle_response(resp)

        # Should not reach here, but just in case
        raise RequestError(0, f"Request failed after {self._settings.max_retries} attempts")

    @staticmethod
    def _backoff(attempt: int) -> None:
        delay = min(2 ** attempt, 30)
        logger.info("Retrying in %ds…", delay)
        time.sleep(delay)

    @staticmethod
    def _handle_response(resp: requests.Response) -> Any:
        if resp.status_code == 204:
            return None

        if not (200 <= resp.status_code < 300):
            try:
                error_info = resp.json()
                message = error_info.get("message", resp.text)
            except Exception:
                message = resp.text
            raise RequestError(resp.status_code, message)

        content_type = resp.headers.get("Content-Type", "").lower()
        binary_types = ("application/pdf", "application/octet-stream", "image/", "application/zip")
        if any(bt in content_type for bt in binary_types):
            return resp.content

        try:
            return resp.json()
        except Exception:
            raise RequestError(resp.status_code, "Response was not valid JSON")
