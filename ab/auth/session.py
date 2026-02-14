"""Django session-based token storage."""

from __future__ import annotations

import logging
from typing import Any, Optional

from ab.auth.base import Token, TokenStorage

logger = logging.getLogger(__name__)

_SESSION_KEY = "ab_token"


class SessionTokenStorage(TokenStorage):
    """Stores tokens in a Django ``request.session``.

    Args:
        request: A Django ``HttpRequest`` whose ``.session`` attribute
            will be used for persistence.
    """

    def __init__(self, request: Any) -> None:
        self._request = request
        self._token: Optional[Token] = None
        self._load()

    def _load(self) -> None:
        data = self._request.session.get(_SESSION_KEY)
        if data:
            try:
                self._token = Token.from_dict(data)
            except Exception:
                logger.warning("Failed to load token from Django session")

    def get_token(self) -> Optional[Token]:
        return self._token

    def save_token(self, token: Token) -> None:
        self._token = token
        self._request.session[_SESSION_KEY] = token.as_dict()

    def clear_token(self) -> None:
        self._token = None
        self._request.session.pop(_SESSION_KEY, None)
