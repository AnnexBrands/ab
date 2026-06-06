"""Parse and validate operator paste exports (captures.json) — feature 037.

Consumed by ``scripts/ingest_captures.py``. Validation-before-write enforces
Constitution II ("no fabricated fixtures"): a pasted response that does not satisfy
its endpoint's pydantic model is a bad paste — surfaced, never written.

Contract: ``specs/037-example-coverage/contracts/captures.schema.json``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ab.progress.example_gen import strip_list_wrapper


@dataclass
class ValidatedCapture:
    """One capture entry after model validation."""

    endpoint: str
    http_method: str
    path: str
    response_model: str  # wrapper-stripped, e.g. "JobPayment"
    request_model: str | None
    ok: bool
    error: str | None
    fixture_name: str | None  # "<Model>.json" or None
    response_json: Any = None  # canonical model_dump (by_alias) ready to write
    request_json: Any = None


def load_captures(path: Path) -> dict[str, dict]:
    """Load captures.json and return the ``captures`` map. Raises ValueError on shape."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != 1:
        raise ValueError("captures.json: missing or unsupported 'schema' (expected 1)")
    captures = data.get("captures")
    if not isinstance(captures, dict):
        raise ValueError("captures.json: 'captures' must be an object")
    return captures


def _model_class(model_name: str):
    import ab.api.models as models_pkg

    return getattr(models_pkg, model_name, None)


def _validate_payload(model_name: str, payload: Any) -> tuple[bool, str | None, Any]:
    """Validate *payload* against the named model; return (ok, error, canonical_json)."""
    if payload is None:
        return False, "no JSON pasted", None
    if isinstance(payload, str):
        return False, "pasted value is not valid JSON (could not parse)", None
    cls = _model_class(model_name)
    if cls is None:
        return False, f"unknown model '{model_name}' in ab.api.models", None
    try:
        if isinstance(payload, list):
            objs = [cls.model_validate(item) for item in payload]
            canonical = [o.model_dump(by_alias=True, mode="json") for o in objs]
        else:
            obj = cls.model_validate(payload)
            canonical = obj.model_dump(by_alias=True, mode="json")
    except Exception as exc:  # pydantic ValidationError or others
        return False, f"{type(exc).__name__}: {str(exc).splitlines()[0]}", None
    return True, None, canonical


def validate_capture(key: str, entry: dict) -> ValidatedCapture:
    """Validate a single capture entry (response, and request if present)."""
    response_model = strip_list_wrapper(entry.get("response_model") or "")
    request_model = entry.get("request_model")
    vc = ValidatedCapture(
        endpoint=entry.get("endpoint", key),
        http_method=entry.get("http_method", ""),
        path=entry.get("path", ""),
        response_model=response_model,
        request_model=request_model,
        ok=False,
        error=None,
        fixture_name=None,
    )

    if not response_model:
        vc.error = "no response_model on capture entry"
        return vc

    ok, error, canonical = _validate_payload(response_model, entry.get("response"))
    if not ok:
        vc.error = error
        return vc

    vc.response_json = canonical
    vc.fixture_name = f"{response_model}.json"

    # Optional request body — validate only if both a model and a payload are present.
    req_payload = entry.get("request")
    if request_model and req_payload not in (None, ""):
        r_ok, r_err, r_canon = _validate_payload(strip_list_wrapper(request_model), req_payload)
        if not r_ok:
            vc.error = f"request body invalid: {r_err}"
            return vc
        vc.request_json = r_canon

    vc.ok = True
    return vc


def validate_all(captures: dict[str, dict]) -> list[ValidatedCapture]:
    """Validate every capture entry."""
    return [validate_capture(key, entry) for key, entry in sorted(captures.items())]
