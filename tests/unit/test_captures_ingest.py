"""Tests for paste validation + ingest (feature 037, T025).

Non-live. Uses a real lightweight model so validation is genuine, and drives the
ingest script against a temp repo tree so no committed fixture is touched.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from ab.progress.captures import load_captures, validate_capture

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _model_with_simple_fields() -> tuple[str, dict]:
    """Find a response model in ab.api.models that validates from a tiny dict.

    Returns (model_name, sample_payload). Picks a model with no required fields so
    the test is robust to model churn.
    """
    import ab.api.models as models_pkg
    from ab.api.models.base import ABConnectBaseModel  # type: ignore

    for name in dir(models_pkg):
        cls = getattr(models_pkg, name)
        if not isinstance(cls, type) or not issubclass(cls, ABConnectBaseModel):
            continue
        required = [f for f, fi in cls.model_fields.items() if fi.is_required()]
        if required:
            continue
        try:
            cls.model_validate({})  # constructs with all-optional fields
        except Exception:
            continue
        return name, {}
    pytest.skip("no all-optional response model available")


def test_load_captures_rejects_bad_schema(tmp_path: Path) -> None:
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"schema": 99, "captures": {}}))
    with pytest.raises(ValueError):
        load_captures(p)


def test_validate_capture_rejects_unparseable_response() -> None:
    vc = validate_capture(
        "api.x.y",
        {"endpoint": "api.x.y", "http_method": "GET", "path": "/x",
         "response_model": "DefinitelyNotAModel", "response": "not json"},
    )
    assert vc.ok is False
    assert vc.error  # string reason, no fixture
    assert vc.fixture_name is None


def test_validate_capture_accepts_valid_model_payload() -> None:
    model_name, payload = _model_with_simple_fields()
    vc = validate_capture(
        "api.notes.list",
        {"endpoint": "api.notes.list", "http_method": "GET", "path": "/notes",
         "response_model": model_name, "response": payload},
    )
    assert vc.ok is True, vc.error
    assert vc.fixture_name == f"{model_name}.json"
    assert vc.response_json is not None


def test_ingest_dry_run_writes_nothing(tmp_path: Path) -> None:
    model_name, payload = _model_with_simple_fields()
    captures = {
        "schema": 1,
        "captures": {
            "api.notes.list": {
                "endpoint": "api.notes.list", "http_method": "GET", "path": "/notes",
                "response_model": model_name, "response": payload,
            }
        },
    }
    cap_file = tmp_path / "captures.json"
    cap_file.write_text(json.dumps(captures))

    proc = subprocess.run(
        [sys.executable, "scripts/ingest_captures.py", str(cap_file), "--dry-run"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ok" in proc.stdout
    assert "dry run" in proc.stdout


def test_ingest_reports_rejection_nonzero(tmp_path: Path) -> None:
    captures = {
        "schema": 1,
        "captures": {
            "api.x.y": {
                "endpoint": "api.x.y", "http_method": "GET", "path": "/x",
                "response_model": "NotARealModel", "response": {"a": 1},
            }
        },
    }
    cap_file = tmp_path / "captures.json"
    cap_file.write_text(json.dumps(captures))
    proc = subprocess.run(
        [sys.executable, "scripts/ingest_captures.py", str(cap_file), "--dry-run"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode == 1
    assert "reject" in proc.stdout
