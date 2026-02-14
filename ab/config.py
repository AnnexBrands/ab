"""Typed configuration via pydantic-settings for the ABConnect SDK."""

from __future__ import annotations

import os
from typing import Literal, Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from ab.exceptions import ConfigurationError


class ABConnectSettings(BaseSettings):
    """SDK configuration loaded from environment variables or .env files.

    Environment variable prefix: ``ABCONNECT_``

    Example ``.env.staging``::

        ABCONNECT_USERNAME=user@example.com
        ABCONNECT_PASSWORD=secret
        ABCONNECT_CLIENT_ID=my-client-id
        ABCONNECT_CLIENT_SECRET=my-client-secret
        ABCONNECT_ENVIRONMENT=staging
    """

    model_config = SettingsConfigDict(
        env_prefix="ABCONNECT_",
        env_file=None,  # set dynamically
        env_file_encoding="utf-8",
        extra="ignore",
    )

    username: str = Field(default="", description="ABConnect username")
    password: str = Field(default="", description="ABConnect password")
    client_id: str = Field(default="", description="OAuth2 client ID")
    client_secret: str = Field(default="", description="OAuth2 client secret")
    environment: Literal["staging", "production"] = Field(
        default="production", description="Target environment"
    )
    access_key: Optional[str] = Field(default=None, description="ABC API access key")
    timeout: int = Field(default=30, description="HTTP request timeout in seconds")
    max_attempts: int = Field(default=3, description="Max total attempts per request (1 initial + retries)")

    @model_validator(mode="after")
    def _validate_required(self) -> "ABConnectSettings":
        missing = []
        if not self.username:
            missing.append("ABCONNECT_USERNAME")
        if not self.password:
            missing.append("ABCONNECT_PASSWORD")
        if not self.client_id:
            missing.append("ABCONNECT_CLIENT_ID")
        if not self.client_secret:
            missing.append("ABCONNECT_CLIENT_SECRET")
        if missing:
            raise ConfigurationError(
                f"Missing required configuration: {', '.join(missing)}. "
                "Set them as environment variables or in your .env file."
            )
        return self

    @property
    def identity_url(self) -> str:
        if self.environment == "staging":
            return "https://login.staging.abconnect.co/connect/token"
        return "https://login.abconnect.co/connect/token"

    @property
    def acportal_base_url(self) -> str:
        if self.environment == "staging":
            return "https://portal.staging.abconnect.co/api/api"
        return "https://portal.abconnect.co/api/api"

    @property
    def catalog_base_url(self) -> str:
        if self.environment == "staging":
            return "https://catalog-api.staging.abconnect.co/api"
        return "https://catalog-api.abconnect.co/api"

    @property
    def abc_base_url(self) -> str:
        if self.environment == "staging":
            return "https://api.staging.abconnect.co/api"
        return "https://api.abconnect.co/api"


def load_settings(
    *,
    env: str | None = None,
    env_file: str | None = None,
) -> ABConnectSettings:
    """Create an :class:`ABConnectSettings` for the given environment.

    Args:
        env: ``"staging"`` or ``"production"``.  When provided the
            corresponding ``.env.{env}`` file is loaded automatically.
        env_file: Explicit path to an env file (overrides *env*).

    Returns:
        Validated settings instance.
    """
    kwargs: dict = {}

    if env_file:
        if os.path.isfile(env_file):
            kwargs["_env_file"] = env_file
    elif env:
        candidate = f".env.{env}"
        if os.path.isfile(candidate):
            kwargs["_env_file"] = candidate
        kwargs["environment"] = env  # type: ignore[arg-type]

    return ABConnectSettings(**kwargs)
