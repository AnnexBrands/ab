"""Shared pytest fixtures and configuration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(model_name: str) -> dict | list:
    """Load a JSON fixture by model name.

    Args:
        model_name: e.g. ``"CompanySimple"`` loads ``tests/fixtures/CompanySimple.json``

    Returns:
        Parsed JSON data.
    """
    path = FIXTURES_DIR / f"{model_name}.json"
    return json.loads(path.read_text())


@pytest.fixture(scope="session")
def fixture_loader():
    """Provide a fixture loader callable to tests."""
    return load_fixture


@pytest.fixture(scope="session")
def api():
    """Session-scoped ABConnectAPI client for live integration tests.

    Requires valid staging credentials in environment or ``.env.staging``.
    Skips the entire session if credentials are unavailable.
    """
    from ab import ABConnectAPI
    from ab.exceptions import ConfigurationError

    try:
        client = ABConnectAPI(env="staging")
    except ConfigurationError:
        pytest.skip("Staging credentials not available")
    return client
