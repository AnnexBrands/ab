"""Validate request fixtures against their corresponding RequestModel classes.

For each JSON file in ``tests/fixtures/requests/``, resolves the
corresponding Pydantic ``RequestModel`` subclass by filename and
calls ``model_validate()`` to confirm the fixture is valid.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ab.api import models

REQUESTS_DIR = Path(__file__).parent.parent / "fixtures" / "requests"


def _discover_request_fixtures() -> list[tuple[str, Path]]:
    """Return (model_name, path) pairs for all request fixture files."""
    if not REQUESTS_DIR.exists():
        return []
    return [
        (p.stem, p)
        for p in sorted(REQUESTS_DIR.glob("*.json"))
        if p.stem != ".gitkeep"
    ]


_FIXTURES = _discover_request_fixtures()


@pytest.mark.parametrize(
    "model_name,fixture_path",
    _FIXTURES,
    ids=[name for name, _ in _FIXTURES],
)
def test_request_fixture_validates(model_name: str, fixture_path: Path) -> None:
    """Load a request fixture and validate it against its RequestModel."""
    model_cls = getattr(models, model_name, None)
    if model_cls is None:
        pytest.skip(
            f"Model {model_name} not found in ab.api.models — "
            f"add the model or rename the fixture"
        )

    data = json.loads(fixture_path.read_text())
    instance = model_cls.model_validate(data)
    assert instance is not None, f"{model_name}.model_validate() returned None"

    # Round-trip: serialized output must also validate
    serialized = instance.model_dump(by_alias=True, exclude_none=True, mode="json")
    model_cls.model_validate(serialized)
