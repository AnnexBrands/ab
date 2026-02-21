"""File-based token storage for standalone (non-Django) usage."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from ab.auth.base import Token, TokenStorage

logger = logging.getLogger(__name__)


class FileTokenStorage(TokenStorage):
    """Stores tokens as JSON in ``~/.cache/ab/token.{env}.json``.

    The environment suffix prevents staging and production tokens from
    contaminating each other.
    """

    def __init__(self, environment: str = "production") -> None:
        cache_dir = Path.home() / ".cache" / "ab"
        cache_dir.mkdir(parents=True, exist_ok=True)
        self._path = cache_dir / f"token.{environment}.json"
        self._token: Optional[Token] = None
        self._load()

    def _load(self) -> None:
        if self._path.is_file():
            try:
                data = json.loads(self._path.read_text())
                self._token = Token.from_dict(data)
            except Exception:
                logger.warning("Failed to load cached token from %s", self._path)
                self._token = None

    def get_token(self) -> Optional[Token]:
        return self._token

    def save_token(self, token: Token) -> None:
        self._token = token
        try:
            self._path.write_text(json.dumps(token.as_dict()))
        except Exception:
            logger.warning("Failed to write token to %s", self._path)

    def clear_token(self) -> None:
        self._token = None
        try:
            self._path.unlink(missing_ok=True)
        except Exception:
            pass
