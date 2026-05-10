"""File-based token storage for standalone (non-Django) usage."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Optional

from ab.auth.base import Token, TokenStorage

logger = logging.getLogger(__name__)


class FileTokenStorage(TokenStorage):
    """Stores tokens as JSON in ``~/.cache/ab/token.{env}.json``.

    The environment suffix prevents staging and production tokens from
    contaminating each other.
    """

    def __init__(
        self,
        environment: str = "production",
        *,
        username: str | None = None,
        client_id: str | None = None,
        token_dir: str | Path | None = None,
    ) -> None:
        cache_dir = Path(token_dir).expanduser() if token_dir is not None else Path.home() / ".cache" / "ab"
        cache_dir.mkdir(parents=True, exist_ok=True)
        self._legacy_path = cache_dir / f"token.{environment}.json"
        scoped_name = self._scoped_filename(environment, username=username, client_id=client_id)
        self._path = cache_dir / scoped_name
        self._token: Optional[Token] = None
        self._load()

    @staticmethod
    def _safe_part(value: str) -> str:
        safe = "".join(ch if ch.isalnum() or ch in ("-", "_", ".", "@") else "_" for ch in value)
        return safe[:120] or "unknown"

    @classmethod
    def _scoped_filename(
        cls,
        environment: str,
        *,
        username: str | None,
        client_id: str | None,
    ) -> str:
        parts = [environment]
        if username:
            parts.append(cls._safe_part(username.lower()))
        if client_id:
            parts.append(cls._safe_part(client_id))
        return f"token.{'.'.join(parts)}.json"

    def _load(self) -> None:
        load_path = self._path
        legacy_path = getattr(self, "_legacy_path", self._path)
        if not load_path.is_file() and legacy_path != self._path and legacy_path.is_file():
            load_path = legacy_path
        if load_path.is_file():
            try:
                data = json.loads(load_path.read_text())
                self._token = Token.from_dict(data)
            except Exception:
                logger.warning("Failed to load cached token from %s", load_path)
                self._token = None

    def get_token(self) -> Optional[Token]:
        return self._token

    def save_token(self, token: Token) -> None:
        self._token = token
        tmp_path = self._path.with_name(f"{self._path.name}.tmp")
        try:
            fd = os.open(tmp_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(json.dumps(token.as_dict()))
            os.replace(tmp_path, self._path)
            os.chmod(self._path, 0o600)
        except Exception:
            logger.warning("Failed to write token to %s", self._path)
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass

    def clear_token(self) -> None:
        self._token = None
        try:
            self._path.unlink(missing_ok=True)
        except Exception:
            pass
