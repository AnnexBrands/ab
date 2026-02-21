"""Abstract token storage and Token dataclass."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Token:
    """Represents an OAuth2 token set."""

    access_token: str
    refresh_token: Optional[str] = None
    expires_at: float = 0.0
    token_type: str = "Bearer"

    @property
    def expired(self) -> bool:
        return time.time() >= self.expires_at

    def as_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
            "token_type": self.token_type,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Token":
        return cls(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            expires_at=data.get("expires_at", 0.0),
            token_type=data.get("token_type", "Bearer"),
        )


class TokenStorage(ABC):
    """Abstract interface for persisting OAuth2 tokens."""

    @abstractmethod
    def get_token(self) -> Optional[Token]:
        """Return the current token, refreshing if necessary."""

    @abstractmethod
    def save_token(self, token: Token) -> None:
        """Persist *token*."""

    @abstractmethod
    def clear_token(self) -> None:
        """Remove any persisted token."""
