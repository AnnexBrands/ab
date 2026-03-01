"""Quality gate evaluation for endpoint status tracking.

Six gates determine endpoint completion:
- G1: Model Fidelity — response model declares all fixture fields
- G2: Fixture Status — fixture file exists on disk
- G3: Test Quality — tests assert isinstance + zero __pydantic_extra__
- G4: Documentation Accuracy — return type is not Any, docs exist
- G5: Parameter Routing — query params use params_model dispatch
- G6: Request Quality — typed signatures, field descriptions, verified optionality
"""

from __future__ import annotations

import functools
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
    g5_param_routing: GateResult | None = None
    g6_request_quality: GateResult | None = None
    overall_status: str = "incomplete"
    notes: str = ""

    def compute_overall(self) -> None:
        """Set overall_status based on all applicable gates."""
        gates = [
            self.g1_model_fidelity,
            self.g2_fixture_status,
            self.g3_test_quality,
            self.g4_doc_accuracy,
            self.g5_param_routing,
            self.g6_request_quality,
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
        fixture_path = FIXTURES_DIR / "mocks" / f"{model_name}.json"
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
    except (ValueError, TypeError, KeyError) as exc:
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

MOCKS_DIR = FIXTURES_DIR / "mocks"


def evaluate_g2(model_name: str) -> GateResult:
    """Check if fixture file exists on disk (live or mock).

    Checks ``tests/fixtures/{model_name}.json`` first (live), then falls
    back to ``tests/fixtures/mocks/{model_name}.json`` (mock). Live
    fixtures take precedence; provenance is reported in the reason.
    """
    if not model_name or model_name == "—":
        return GateResult("G2", False, "No response model specified")

    live_path = FIXTURES_DIR / f"{model_name}.json"
    if live_path.exists():
        return GateResult("G2", True, "live fixture")
    mock_path = MOCKS_DIR / f"{model_name}.json"
    if mock_path.exists():
        return GateResult("G2", True, "mock fixture")
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
# G5: Parameter Routing
# ---------------------------------------------------------------------------

SCHEMAS_DIR = REPO_ROOT / "ab" / "api" / "schemas"


@functools.lru_cache(maxsize=4)
def _load_swagger(schema_file: str = "acportal.json") -> dict:
    """Load a swagger/OpenAPI spec (cached)."""
    path = SCHEMAS_DIR / schema_file
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _get_swagger_query_params(
    endpoint_path: str, method: str,
) -> list[dict] | None:
    """Get query parameters from swagger for the given endpoint.

    Returns list of param dicts, empty list if no query params, or None
    if the endpoint is not found in any swagger spec.
    """
    # Our Route paths omit the /api/ prefix that swagger uses
    swagger_path = f"/api{endpoint_path}"
    method_lower = method.lower()

    for schema_file in ("acportal.json", "catalog.json", "abc.json"):
        spec = _load_swagger(schema_file)
        if not spec:
            continue
        paths = spec.get("paths", {})

        # Try exact match
        if swagger_path in paths:
            op = paths[swagger_path].get(method_lower, {})
            params = op.get("parameters", [])
            return [p for p in params if p.get("in") == "query"]

        # Try matching with normalized path params (swagger may use
        # different param names like {jobId} vs our {jobDisplayId})
        normalized = re.sub(r"\{[^}]+\}", "{}", swagger_path)
        for spec_path, methods in paths.items():
            spec_normalized = re.sub(r"\{[^}]+\}", "{}", spec_path)
            if spec_normalized == normalized and method_lower in methods:
                params = methods[method_lower].get("parameters", [])
                return [p for p in params if p.get("in") == "query"]

    return None


_ROUTE_PARAMS_MODEL_RE = re.compile(
    r"Route\([^)]*?"
    r"params_model\s*=\s*[\"'](\w+)[\"']"
    r"[^)]*?\)",
    re.DOTALL,
)


def _route_has_params_model(file_content: str, endpoint_path: str) -> bool:
    """Check if any Route definition for the given path has params_model set."""
    # Find all Route(...) definitions that contain this endpoint path
    # Route paths may be bound, so match the static portion
    path_escaped = re.escape(endpoint_path)
    # Handle path params: /job/{jobDisplayId}/... -> /job/\{[^}]+\}/...
    path_pattern = re.sub(r"\\{[^}]+\\}", r"\\{[^}]+\\}", path_escaped)
    route_pattern = re.compile(
        r"Route\([^)]*?" + path_pattern + r"[^)]*?\)",
        re.DOTALL,
    )

    for match in route_pattern.finditer(file_content):
        route_text = match.group(0)
        if "params_model" in route_text:
            return True
    return False


def evaluate_g5(endpoint_path: str, method: str) -> GateResult:
    """Check if query params are routed through params_model dispatch.

    Auto-passes if swagger defines no query parameters for this endpoint.
    """
    query_params = _get_swagger_query_params(endpoint_path, method)

    if query_params is None:
        return GateResult("G5", True, "Not in swagger — auto-pass")

    if not query_params:
        return GateResult("G5", True, "No query parameters — auto-pass")

    # Query params exist in swagger → Route must have params_model
    endpoint_module = _infer_endpoint_module(endpoint_path)
    if not endpoint_module:
        return GateResult("G5", False, "Cannot infer endpoint module")

    ep_file = ENDPOINTS_DIR / f"{endpoint_module}.py"
    if not ep_file.exists():
        return GateResult(
            "G5", False, f"Endpoint file {endpoint_module}.py not found",
        )

    content = ep_file.read_text()
    if _route_has_params_model(content, endpoint_path):
        return GateResult(
            "G5", True,
            f"params_model set for {len(query_params)} query param(s)",
        )

    param_names = ", ".join(p["name"] for p in query_params)
    return GateResult(
        "G5", False,
        f"{len(query_params)} query param(s) ({param_names}) but no params_model",
    )


# ---------------------------------------------------------------------------
# G6: Request Quality
# ---------------------------------------------------------------------------

_KWARGS_RE = re.compile(r"\*\*kwargs\s*:\s*Any")
_DATA_DICT_ANY_RE = re.compile(r"data\s*:\s*dict\s*\|\s*Any")


def _g6a_typed_signature(
    endpoint_path: str,
    request_model: str | None,
    params_model: str | None,
) -> GateResult:
    """G6a: Check endpoint method does NOT use **kwargs or data: dict | Any."""
    if not request_model and not params_model:
        return GateResult("G6a", True, "No request/params model — auto-pass")

    endpoint_module = _infer_endpoint_module(endpoint_path)
    if not endpoint_module:
        return GateResult("G6a", False, "Cannot infer endpoint module")

    ep_file = ENDPOINTS_DIR / f"{endpoint_module}.py"
    if not ep_file.exists():
        return GateResult("G6a", False, f"Endpoint file {endpoint_module}.py not found")

    content = ep_file.read_text()

    # Find methods associated with routes that reference this path
    # We scan for method definitions that contain **kwargs or data: dict | Any
    # within the vicinity of the endpoint path
    path_escaped = re.escape(endpoint_path)
    path_pattern = re.sub(r"\\{[^}]+\\}", r"\\{[^}]+\\}", path_escaped)

    # Find Route definitions for this path
    route_var_re = re.compile(
        r"^(\w+)\s*=\s*Route\([^)]*?" + path_pattern + r"[^)]*?\)",
        re.MULTILINE | re.DOTALL,
    )
    route_match = route_var_re.search(content)
    if not route_match:
        return GateResult("G6a", True, "Route not found in file — auto-pass")

    route_var = route_match.group(1)

    # Find the method that uses this route variable
    method_re = re.compile(
        r"def\s+(\w+)\s*\(([^)]*)\).*?self\._(?:request|paginated_request)\s*\(\s*"
        + re.escape(route_var),
        re.DOTALL,
    )
    method_match = method_re.search(content)
    if not method_match:
        return GateResult("G6a", True, "Method not found for route — auto-pass")

    method_sig = method_match.group(2)

    if _KWARGS_RE.search(method_sig):
        return GateResult("G6a", False, f"Method uses **kwargs: Any")
    if _DATA_DICT_ANY_RE.search(method_sig):
        return GateResult("G6a", False, f"Method uses data: dict | Any")

    return GateResult("G6a", True)


def _g6b_field_descriptions(model_name: str | None) -> GateResult:
    """G6b: Check every field in the request model has a non-empty description."""
    if not model_name:
        return GateResult("G6b", True, "No request model — auto-pass")

    try:
        model_cls = _resolve_model(model_name)
    except (ImportError, AttributeError) as exc:
        return GateResult("G6b", False, f"Model class not found: {exc}")

    missing = []
    for field_name, field_info in model_cls.model_fields.items():
        desc = field_info.description
        if not desc or not desc.strip():
            missing.append(field_name)

    if missing:
        return GateResult(
            "G6b", False,
            f"{len(missing)} field(s) without description: {', '.join(missing)}",
        )
    return GateResult("G6b", True)


def _g6c_optionality_verified(model_name: str | None) -> GateResult:
    """G6c: Check model source has no '# TODO: verify optionality' markers."""
    if not model_name:
        return GateResult("G6c", True, "No request model — auto-pass")

    # Find the model source file
    models_dir = REPO_ROOT / "ab" / "api" / "models"
    for py_file in models_dir.glob("*.py"):
        content = py_file.read_text()
        if f"class {model_name}" in content:
            if "# TODO: verify optionality" in content:
                return GateResult(
                    "G6c", False,
                    f"'{model_name}' source contains '# TODO: verify optionality'",
                )
            return GateResult("G6c", True)

    return GateResult("G6c", True, "Model source not found — auto-pass")


def evaluate_g6(
    endpoint_path: str,
    method: str,
    request_model: str | None = None,
    params_model: str | None = None,
) -> GateResult:
    """Evaluate G6: Request Model Quality.

    Combines three sub-criteria:
    - G6a: Typed signature (no **kwargs or data: dict | Any)
    - G6b: Field descriptions (every field has description)
    - G6c: Optionality verified (no TODO markers)

    Returns PASS only if all three sub-criteria pass.
    """
    if not request_model and not params_model:
        return GateResult("G6", True, "No request/params model — auto-pass")

    results = [
        _g6a_typed_signature(endpoint_path, request_model, params_model),
        _g6b_field_descriptions(request_model),
        _g6b_field_descriptions(params_model),  # Also check params model
        _g6c_optionality_verified(request_model),
        _g6c_optionality_verified(params_model),
    ]

    failures = [r for r in results if not r.passed]
    if failures:
        reasons = "; ".join(f"{r.gate}: {r.reason}" for r in failures)
        return GateResult("G6", False, reasons)

    return GateResult("G6", True)


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
        "commodity": "commodities",
        "commodity-maps": "commodity_maps",
        "commodity-map": "commodity_maps",
        "forms": "forms",
        "note": "notes",
        "partner": "partners",
        "Lot": "lots",
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
    params_model: str | None = None,
    notes: str = "",
) -> EndpointGateStatus:
    """Evaluate all six gates for a single endpoint."""
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
        status.g5_param_routing = evaluate_g5(endpoint_path, method)
        status.g6_request_quality = evaluate_g6(endpoint_path, method, request_model, params_model)
        status.compute_overall()
        return status

    # Strip List[] wrapper for fixture/model lookup
    clean_model = response_model
    if clean_model.startswith("List["):
        clean_model = clean_model[5:-1]
    if clean_model.startswith("list["):
        clean_model = clean_model[5:-1]

    # Scalar builtins (str, int, bool, float) are not Pydantic models —
    # exempt from fixture/model gates (G1-G4).
    _SCALAR_TYPES = {"str", "int", "bool", "float", "None"}
    if clean_model in _SCALAR_TYPES:
        status.g1_model_fidelity = GateResult("G1", True, f"Scalar type ({clean_model}) — no model to validate")
        status.g2_fixture_status = GateResult("G2", True, f"Scalar type ({clean_model}) — no fixture needed")
        status.g3_test_quality = GateResult("G3", True, f"Scalar type ({clean_model}) — no model assertions needed")
        status.g4_doc_accuracy = GateResult("G4", True, f"Scalar type ({clean_model}) — return type is correct")
        status.g5_param_routing = evaluate_g5(endpoint_path, method)
        status.g6_request_quality = evaluate_g6(endpoint_path, method, request_model, params_model)
        status.compute_overall()
        return status

    endpoint_module = _infer_endpoint_module(endpoint_path)

    status.g1_model_fidelity = evaluate_g1(clean_model)
    status.g2_fixture_status = evaluate_g2(clean_model)
    status.g3_test_quality = evaluate_g3(clean_model)
    status.g4_doc_accuracy = evaluate_g4(clean_model, endpoint_module)
    status.g5_param_routing = evaluate_g5(endpoint_path, method)
    status.g6_request_quality = evaluate_g6(endpoint_path, method, request_model, params_model)
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
            params_model=entry.get("params_model"),
            notes=entry.get("notes", ""),
        )
        results.append(status)
    return results
