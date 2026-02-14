"""Shared pytest fixtures and configuration."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(model_name: str) -> dict | list:
    """Load a JSON fixture by model name.

    Args:
        model_name: e.g. ``"CompanySimple"`` loads ``tests/fixtures/CompanySimple.json``

    Returns:
        Parsed JSON data.

    Raises:
        FileNotFoundError: If fixture file does not exist.
    """
    path = FIXTURES_DIR / f"{model_name}.json"
    return json.loads(path.read_text())


def require_fixture(
    model_name: str,
    method: str = "",
    path: str = "",
    *,
    required: bool = False,
) -> dict | list:
    """Load a fixture, or skip/fail when it is missing.

    Args:
        model_name: e.g. ``"CompanySimple"``
        method: HTTP method, e.g. ``"GET"``
        path: API endpoint path, e.g. ``"/companies/{id}"``
        required: If ``True``, a missing fixture **fails** the test
            (use for previously captured live fixtures). If ``False``
            (default), a missing fixture **skips** with capture
            instructions (use for pending fixtures).

    Returns:
        Parsed JSON data (when fixture exists).
    """
    fixture_path = FIXTURES_DIR / f"{model_name}.json"
    if not fixture_path.exists():
        if required:
            pytest.fail(
                f"Required fixture missing: {model_name}.json — "
                f"this was previously captured and must not be deleted"
            )
        msg = f"Fixture needed: capture {model_name}.json"
        if method and path:
            msg += f" via {method} {path}"
        pytest.skip(msg)
    return load_fixture(model_name)


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
