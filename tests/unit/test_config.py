"""Unit tests for ABConnectSettings (T049)."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from ab.config import ABConnectSettings, load_settings
from ab.exceptions import ConfigurationError


_VALID_ENV = {
    "ABCONNECT_USERNAME": "testuser",
    "ABCONNECT_PASSWORD": "testpass",
    "ABCONNECT_CLIENT_ID": "cid",
    "ABCONNECT_CLIENT_SECRET": "csecret",
}


class TestABConnectSettings:
    def test_loads_from_env_vars(self):
        with patch.dict(os.environ, _VALID_ENV, clear=False):
            settings = ABConnectSettings()
        assert settings.username == "testuser"
        assert settings.password == "testpass"
        assert settings.client_id == "cid"
        assert settings.client_secret == "csecret"
        assert settings.environment == "production"

    def test_default_timeout_and_attempts(self):
        with patch.dict(os.environ, _VALID_ENV, clear=False):
            settings = ABConnectSettings()
        assert settings.timeout == 30
        assert settings.max_attempts == 3

    def test_staging_environment(self):
        env = {**_VALID_ENV, "ABCONNECT_ENVIRONMENT": "staging"}
        with patch.dict(os.environ, env, clear=False):
            settings = ABConnectSettings()
        assert settings.environment == "staging"
        assert "staging" in settings.identity_url
        assert "staging" in settings.acportal_base_url
        assert "staging" in settings.catalog_base_url
        assert "staging" in settings.abc_base_url

    def test_production_urls(self):
        with patch.dict(os.environ, _VALID_ENV, clear=False):
            settings = ABConnectSettings()
        assert settings.identity_url == "https://login.abconnect.co/connect/token"
        assert settings.acportal_base_url == "https://portal.abconnect.co/api/api"
        assert settings.catalog_base_url == "https://catalog-api.abconnect.co/api"
        assert settings.abc_base_url == "https://api.abconnect.co/api"

    def test_raises_on_missing_username(self):
        env = {k: v for k, v in _VALID_ENV.items() if k != "ABCONNECT_USERNAME"}
        with patch.dict(os.environ, env, clear=True):
            with pytest.raises(ConfigurationError, match="ABCONNECT_USERNAME"):
                ABConnectSettings()

    def test_raises_on_missing_multiple(self):
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ConfigurationError, match="ABCONNECT_USERNAME"):
                ABConnectSettings()

    def test_load_settings_with_env(self, tmp_path):
        env_file = tmp_path / ".env.staging"
        env_file.write_text(
            "ABCONNECT_USERNAME=u\n"
            "ABCONNECT_PASSWORD=p\n"
            "ABCONNECT_CLIENT_ID=c\n"
            "ABCONNECT_CLIENT_SECRET=s\n"
            "ABCONNECT_ENVIRONMENT=staging\n"
        )
        with patch.dict(os.environ, {}, clear=True):
            settings = load_settings(env_file=str(env_file))
        assert settings.username == "u"
        assert settings.environment == "staging"
