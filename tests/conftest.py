"""Shared pytest fixtures and configuration."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
MOCKS_DIR = FIXTURES_DIR / "mocks"


def _resolve_fixture_path(model_name: str) -> Path | None:
    """Find fixture file, checking live directory first then mocks/.

    Returns the path if found, or None if neither exists.
    """
    live_path = FIXTURES_DIR / f"{model_name}.json"
    if live_path.exists():
        return live_path
    mock_path = MOCKS_DIR / f"{model_name}.json"
    if mock_path.exists():
        return mock_path
    return None


def load_fixture(model_name: str) -> dict | list:
    """Load a JSON fixture by model name.

    Checks ``tests/fixtures/{model_name}.json`` first (live), then falls
    back to ``tests/fixtures/mocks/{model_name}.json`` (mock). Live
    fixtures always take precedence.

    Args:
        model_name: e.g. ``"CompanySimple"`` loads ``tests/fixtures/CompanySimple.json``
            or ``tests/fixtures/mocks/CompanySimple.json``

    Returns:
        Parsed JSON data.

    Raises:
        FileNotFoundError: If fixture file does not exist in either location.
    """
    path = _resolve_fixture_path(model_name)
    if path is None:
        raise FileNotFoundError(
            f"Fixture not found: checked {FIXTURES_DIR / f'{model_name}.json'} "
            f"and {MOCKS_DIR / f'{model_name}.json'}"
        ) from None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in fixture {model_name}.json: {exc}") from exc


def require_fixture(
    model_name: str,
    method: str = "",
    path: str = "",
    *,
    required: bool = False,
) -> dict | list:
    """Load a fixture, or skip/fail when it is missing.

    Checks both live (``tests/fixtures/``) and mock (``tests/fixtures/mocks/``)
    directories. Live fixtures take precedence.

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
    fixture_path = _resolve_fixture_path(model_name)
    if fixture_path is None:
        if required:
            pytest.fail(
                f"Required fixture missing: {model_name}.json — "
                f"checked {FIXTURES_DIR} and {MOCKS_DIR}"
            )
        msg = f"Fixture needed: capture {model_name}.json"
        if method and path:
            msg += f" via {method} {path}"
        pytest.skip(msg)
    return load_fixture(model_name)


def assert_no_extra_fields(model: object) -> None:
    """Assert a Pydantic model has no undeclared extra fields.

    Args:
        model: A Pydantic model instance (ResponseModel subclass).

    Raises:
        AssertionError: If ``model.__pydantic_extra__`` is non-empty,
            with a message listing all undeclared field names.
    """
    extra = getattr(model, "__pydantic_extra__", None)
    if extra:
        cls_name = model.__class__.__name__
        fields = ", ".join(sorted(extra.keys()))
        assert not extra, (
            f"{cls_name} has {len(extra)} undeclared extra field(s): {fields}"
        )


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
