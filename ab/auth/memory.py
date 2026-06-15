"""In-memory token storage — process-local, never persisted."""

from __future__ import annotations

from typing import Optional

from ab.auth.base import Token, TokenStorage


class MemoryTokenStorage(TokenStorage):
    """Holds a single :class:`Token` in memory.

    Useful for workers acting as a snapshotted identity (seed the storage
    with an existing token), for tests, and for anonymous clients (leave it
    empty). Nothing is written to disk or any session backend; the token
    lives and dies with this object.

    >>> storage = MemoryTokenStorage()                 # empty (anonymous)
    >>> storage = MemoryTokenStorage(token=my_token)   # seeded worker identity
    """

    def __init__(self, token: Optional[Token] = None) -> None:
        self._token = token

    def get_token(self) -> Optional[Token]:
        return self._token

    def save_token(self, token: Token) -> None:
        self._token = token

    def clear_token(self) -> None:
        self._token = None
