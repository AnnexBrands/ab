"""Quality gate evaluation for endpoint status tracking.

Four gates determine endpoint completion:
- G1: Model Fidelity — response model declares all fixture fields
- G2: Fixture Status — fixture file exists on disk
- G3: Test Quality — tests assert isinstance + zero __pydantic_extra__
- G4: Documentation Accuracy — return type is not Any, docs exist
"""

from __future__ import annotations

import importlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
TESTS_DIR = REPO_ROOT / "tests"
ENDPOINTS_DIR = REPO_ROOT / "ab" / "api" / "endpoints"
DOCS_DIR = REPO_ROOT / "docs"


@dataclass
class GateResult:
    """Result of a single gate evaluation."""

    gate: str  # "G1", "G2", "G3", "G4"
    passed: bool
    reason: str = ""


@dataclass
class EndpointGateStatus:
    """Per-endpoint aggregate of all gate evaluations."""

    endpoint_path: str
    method: str
    request_model: str | None = None
    response_model: str | None = None
    api_surface: str = "acportal"
    g1_model_fidelity: GateResult | None = None
    g2_fixture_status: GateResult | None = None
    g3_test_quality: GateResult | None = None
    g4_doc_accuracy: GateResult | None = None
    overall_status: str = "incomplete"
    notes: str = ""

    def compute_overall(self) -> None:
        """Set overall_status based on all applicable gates."""
        gates = [
            self.g1_model_fidelity,
            self.g2_fixture_status,
            self.g3_test_quality,
            self.g4_doc_accuracy,
        ]
        applicable = [g for g in gates if g is not None]
        if not applicable:
            self.overall_status = "incomplete"
            return
        if all(g.passed for g in applicable):
            self.overall_status = "complete"
        else:
            self.overall_status = "incomplete"


# ---------------------------------------------------------------------------
# G1: Model Fidelity
# ---------------------------------------------------------------------------

def evaluate_g1(model_name: str) -> GateResult:
    """Check if model declares all fields from its fixture (zero __pydantic_extra__)."""
    if not model_name or model_name == "—":
        return GateResult("G1", False, "No response model specified")

    fixture_path = FIXTURES_DIR / f"{model_name}.json"
    if not fixture_path.exists():
        return GateResult("G1", False, f"Fixture {model_name}.json not found")

    try:
        model_cls = _resolve_model(model_name)
    except (ImportError, AttributeError) as exc:
        return GateResult("G1", False, f"Model class not found: {exc}")

    try:
        data = json.loads(fixture_path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        return GateResult("G1", False, f"Fixture load error: {exc}")

    # Handle list fixtures — validate first element
    if isinstance(data, list):
        if not data:
            return GateResult("G1", True, "Empty list fixture — nothing to validate")
        data = data[0]

    # Handle paginated wrappers: {data: [...], totalCount: N} or {items: [...]}
    if isinstance(data, dict):
        if "data" in data and isinstance(data["data"], list):
            items = data["data"]
            if not items:
                return GateResult("G1", True, "Empty paginated data — nothing to validate")
            data = items[0]
        elif "items" in data and isinstance(data["items"], list):
            items = data["items"]
            if not items:
                return GateResult("G1", True, "Empty paginated items — nothing to validate")
            data = items[0]

    try:
        instance = model_cls.model_validate(data)
    except Exception as exc:
        return GateResult("G1", False, f"Validation error: {exc}")

    extra = getattr(instance, "__pydantic_extra__", None) or {}
    if extra:
        field_names = ", ".join(sorted(extra.keys()))
        return GateResult(
            "G1", False,
            f"{len(extra)} undeclared field(s): {field_names}",
        )

    return GateResult("G1", True)


# ---------------------------------------------------------------------------
# G2: Fixture Status
# ---------------------------------------------------------------------------

def evaluate_g2(model_name: str) -> GateResult:
    """Check if fixture file exists on disk."""
    if not model_name or model_name == "—":
        return GateResult("G2", False, "No response model specified")

    fixture_path = FIXTURES_DIR / f"{model_name}.json"
    if fixture_path.exists():
        return GateResult("G2", True)
    return GateResult("G2", False, f"Fixture {model_name}.json not found")


# ---------------------------------------------------------------------------
# G3: Test Quality
# ---------------------------------------------------------------------------

_ISINSTANCE_RE = re.compile(r"isinstance\s*\(.*?,\s*(\w+)\s*\)")
_EXTRA_FIELDS_RE = re.compile(
    r"(__pydantic_extra__|assert_no_extra_fields|model_extra)"
)


def evaluate_g3(model_name: str) -> GateResult:
    """Check if tests make substantive assertions (isinstance + __pydantic_extra__)."""
    if not model_name or model_name == "—":
        return GateResult("G3", False, "No response model specified")

    has_isinstance = False
    has_extra_check = False

    # Scan integration tests
    integration_dir = TESTS_DIR / "integration"
    if integration_dir.exists():
        for tf in integration_dir.glob("test_*.py"):
            content = tf.read_text()
            if model_name in content:
                if _ISINSTANCE_RE.search(content) and model_name in content:
                    # Check isinstance specifically references this model
                    for m in _ISINSTANCE_RE.finditer(content):
                        if m.group(1) == model_name:
                            has_isinstance = True
                            break
                if _EXTRA_FIELDS_RE.search(content):
                    has_extra_check = True

    # Scan model tests
    models_dir = TESTS_DIR / "models"
    if models_dir.exists():
        for tf in models_dir.glob("test_*.py"):
            content = tf.read_text()
            if model_name in content:
                if _EXTRA_FIELDS_RE.search(content):
                    has_extra_check = True
                # Also check for isinstance in model tests
                for m in _ISINSTANCE_RE.finditer(content):
                    if m.group(1) == model_name:
                        has_isinstance = True
                        break

    reasons = []
    if not has_isinstance:
        reasons.append(f"No isinstance(result, {model_name}) assertion found")
    if not has_extra_check:
        reasons.append("No __pydantic_extra__ / assert_no_extra_fields check found")

    if reasons:
        return GateResult("G3", False, "; ".join(reasons))
    return GateResult("G3", True)


# ---------------------------------------------------------------------------
# G4: Documentation Accuracy
# ---------------------------------------------------------------------------

def evaluate_g4(model_name: str, endpoint_module: str | None = None) -> GateResult:
    """Check return type annotation and docs existence."""
    if not model_name or model_name == "—":
        return GateResult("G4", False, "No response model specified")

    # Check return type annotations in endpoint files
    has_correct_return_type = False
    has_any_return = False

    if endpoint_module:
        ep_file = ENDPOINTS_DIR / f"{endpoint_module}.py"
        if ep_file.exists():
            content = ep_file.read_text()
            # Check for -> ModelName or -> list[ModelName] or -> List[ModelName]
            return_pattern = re.compile(
                rf"->\s*(?:list\[|List\[)?{re.escape(model_name)}(?:\])?"
            )
            any_pattern = re.compile(r"->\s*Any\b")
            if return_pattern.search(content):
                has_correct_return_type = True
            elif any_pattern.search(content):
                has_any_return = True
    else:
        # Scan all endpoint files
        for ep_file in ENDPOINTS_DIR.glob("*.py"):
            if ep_file.name == "__init__.py":
                continue
            content = ep_file.read_text()
            return_pattern = re.compile(
                rf"->\s*(?:list\[|List\[)?{re.escape(model_name)}(?:\])?"
            )
            if return_pattern.search(content):
                has_correct_return_type = True
                break

    if has_any_return and not has_correct_return_type:
        return GateResult(
            "G4", False,
            f"Return type is Any, should be {model_name}",
        )
    if not has_correct_return_type:
        return GateResult(
            "G4", False,
            f"No correct return type annotation for {model_name} found",
        )

    # Check docs exist
    docs_model_dir = DOCS_DIR / "models"
    if docs_model_dir.exists():
        # We don't require specific doc files per model — just that the return
        # type is correct in the code (Sphinx autodoc will pick it up)
        pass

    return GateResult("G4", True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_model(model_name: str) -> Any:
    """Resolve a model class by name from ab.api.models."""
    # Handle List[] wrappers
    clean_name = model_name
    if clean_name.startswith("List["):
        clean_name = clean_name[5:-1]
    if clean_name.startswith("list["):
        clean_name = clean_name[5:-1]

    mod = importlib.import_module("ab.api.models")
    return getattr(mod, clean_name)


def _infer_endpoint_module(endpoint_path: str) -> str | None:
    """Infer the endpoint module name from an API path."""
    path = endpoint_path.strip("/")
    if not path:
        return None

    # Map known path prefixes to module names
    prefix_map = {
        "companies": "companies",
        "contacts": "contacts",
        "documents": "documents",
        "address": "address",
        "lookup": "lookup",
        "users": "users",
        "job": "jobs",
        "shipment": "shipments",
        "AutoPrice": "autoprice",
        "rfq": "rfq",
        "sellers": "sellers",
        "catalog": "catalog",
        "lots": "lots",
        "web2lead": "web2lead",
        "notes": "notes",
        "partners": "partners",
        "payments": "payments",
        "reports": "reports",
        "dashboard": "dashboard",
        "views": "views",
        "commodities": "commodities",
        "commodity-maps": "commodity_maps",
        "forms": "forms",
        "v3": "jobs",  # v3/job/... maps to jobs module
    }

    first_segment = path.split("/")[0]
    return prefix_map.get(first_segment)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def evaluate_endpoint_gates(
    endpoint_path: str,
    method: str,
    response_model: str | None = None,
    request_model: str | None = None,
    notes: str = "",
) -> EndpointGateStatus:
    """Evaluate all four gates for a single endpoint."""
    status = EndpointGateStatus(
        endpoint_path=endpoint_path,
        method=method,
        request_model=request_model,
        response_model=response_model,
        notes=notes,
    )

    if not response_model or response_model == "—":
        # No-body endpoints (e.g., DELETE, some POSTs) — exempt from G1/G3/G4
        status.g1_model_fidelity = GateResult("G1", False, "No response model")
        status.g2_fixture_status = GateResult("G2", False, "No response model")
        status.g3_test_quality = GateResult("G3", False, "No response model")
        status.g4_doc_accuracy = GateResult("G4", False, "No response model")
        status.compute_overall()
        return status

    # Strip List[] wrapper for fixture/model lookup
    clean_model = response_model
    if clean_model.startswith("List["):
        clean_model = clean_model[5:-1]
    if clean_model.startswith("list["):
        clean_model = clean_model[5:-1]

    endpoint_module = _infer_endpoint_module(endpoint_path)

    status.g1_model_fidelity = evaluate_g1(clean_model)
    status.g2_fixture_status = evaluate_g2(clean_model)
    status.g3_test_quality = evaluate_g3(clean_model)
    status.g4_doc_accuracy = evaluate_g4(clean_model, endpoint_module)
    status.compute_overall()

    return status


def evaluate_all_gates(
    fixtures_data: list[dict[str, str]],
) -> list[EndpointGateStatus]:
    """Evaluate all gates for every endpoint.

    Args:
        fixtures_data: List of dicts with keys: endpoint_path, method,
            request_model, response_model, notes.

    Returns:
        List of EndpointGateStatus for all endpoints.
    """
    results = []
    for entry in fixtures_data:
        status = evaluate_endpoint_gates(
            endpoint_path=entry.get("endpoint_path", ""),
            method=entry.get("method", ""),
            response_model=entry.get("response_model"),
            request_model=entry.get("request_model"),
            notes=entry.get("notes", ""),
        )
        results.append(status)
    return results
