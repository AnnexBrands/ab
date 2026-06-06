"""Internal dataclasses for progress report generation."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.progress.gates import EndpointGateStatus


class RunStatus(str, Enum):
    """Per-endpoint run-and-verify status for the progress report.

    Single source of truth shared by the report column, the coverage gate, and the
    committed ``tests/example_run_results.json`` artifact. See
    ``specs/037-example-coverage/data-model.md``.
    """

    #: Example ran (or paste ingested) and output matches the fixture.
    PASSING = "passing"
    #: Read-only example ran but output != fixture (after volatile normalization).
    FAILING = "failing"
    #: GET with an example and a fixture, but no live-run result yet (not run).
    NOT_VERIFIED = "not_verified"
    #: GET with an example but no fixture / no usable TEST_* constant — can't verify.
    AWAITING_DATA = "awaiting_data"
    #: Mutating endpoint (POST/PUT/PATCH/DELETE) — never auto-run; needs a paste.
    AWAITING_PASTE = "awaiting_paste"
    #: Response is bytes / no-content — covered-as-binary, excluded from comparison.
    BINARY = "binary"
    #: No canonical example exists for the endpoint.
    MISSING_EXAMPLE = "missing_example"

    @property
    def is_covered(self) -> bool:
        """True when the endpoint has *some* canonical example (gate passes)."""
        return self is not RunStatus.MISSING_EXAMPLE

    @property
    def is_green(self) -> bool:
        """True when the endpoint is verified passing."""
        return self is RunStatus.PASSING


#: No-content / raw-bytes response models (excluded from JSON comparison, D10).
#: NB ``""``/``none`` cover void mutation responses on purpose; ``any`` is NOT here —
#: an ``Any`` response is untyped JSON and should still be verifiable.
_BINARY_MODELS = {"", "bytes", "none"}
#: Model names that *end* in a binary/file token (boundary match, not bare substring —
#: so ``UserProfile``/``PdfReport``/``StreamSettings`` are not misclassified).
_BINARY_SUFFIX_RE = re.compile(r"(?:File|Stream|Download|Pdf|Blob|Bytes)$")


def is_binary_response(response_model: str | None) -> bool:
    """Heuristic: does this route return bytes / no JSON-able body? (feature 037, D10)

    Conservative — the clearly no-content/bytes cases, plus names that *end* in a
    file/stream/download token. Refined as real endpoints surface.
    """
    name = (response_model or "").strip()
    if name.lower() in _BINARY_MODELS:
        return True
    return bool(_BINARY_SUFFIX_RE.search(name))


def derive_run_status(
    *,
    http_method: str,
    has_canonical_example: bool,
    response_model: str | None,
    fixture_exists: bool,
) -> "RunStatus":
    """Derive the *expected* run status from code + fixtures (no live result).

    The report overlays the committed run-results artifact on top of this; this is
    what shows when an endpoint has not been verified yet.
    """
    if not has_canonical_example:
        return RunStatus.MISSING_EXAMPLE
    if is_binary_response(response_model):
        return RunStatus.BINARY
    if (http_method or "").upper() != "GET":
        return RunStatus.AWAITING_PASTE
    if not fixture_exists:
        return RunStatus.AWAITING_DATA
    return RunStatus.NOT_VERIFIED


@dataclass
class Endpoint:
    """A single API route from api-surface.md."""

    group_name: str
    api_surface: str
    index: int
    route_key: str
    method: str
    path: str
    response_model: str
    ab_status: str  # "done", "pending", "not_started"
    ref_status: str  # "JSON", "PDF", "none"


@dataclass
class EndpointGroup:
    """Aggregated endpoint group with summary metadata."""

    name: str
    api_surface: str
    endpoints: list[Endpoint] = field(default_factory=list)
    total: int = 0
    done: int = 0
    pending: int = 0
    not_started: int = 0
    ab_file: str | None = None
    ref_file: str | None = None
    priority: str | None = None

    def recount(self) -> None:
        """Recalculate counts from endpoints list."""
        self.total = len(self.endpoints)
        self.done = sum(1 for e in self.endpoints if e.ab_status == "done")
        self.pending = sum(1 for e in self.endpoints if e.ab_status == "pending")
        self.not_started = sum(
            1 for e in self.endpoints if e.ab_status == "not_started"
        )


@dataclass
class Fixture:
    """A fixture entry from FIXTURES.md."""

    endpoint_path: str
    method: str
    model_name: str
    status: str  # "captured", "needs-request-data", or "partial"
    capture_date: str | None = None
    source: str | None = None
    blocker: str | None = None  # "What's Missing" or "Access Required"
    ref: str | None = None
    request_model: str | None = None
    request_fixture_status: str | None = None  # "captured", "needs-data", or None


@dataclass
class Constant:
    """A test constant from tests/constants.py."""

    name: str
    value: str
    value_type: str  # "uuid", "int", "str"


@dataclass
class ActionItem:
    """Enriched view of an unimplemented endpoint for rendering."""

    endpoint: Endpoint
    tier: int  # 1 = scaffolded, 2 = not started
    fixture: Fixture | None = None
    fixture_exists: bool = False
    blocker_type: str = "not_implemented"
    instructions: list[str] = field(default_factory=list)
    required_constants: list[str] = field(default_factory=list)
    missing_constants: list[str] = field(default_factory=list)


@dataclass
class MethodProgress:
    """Unified view of a single endpoint method's coverage."""

    dotted_path: str
    method_name: str
    http_method: str
    http_path: str
    return_type: str
    has_example: bool
    has_cli: bool
    has_route: bool
    path_sub_root: str
    has_docstring: bool = True
    gate_status: EndpointGateStatus | None = None
    # Run-and-verify (feature 037). run_status defaults to MISSING_EXAMPLE and is
    # overwritten by the report builder from the run-results artifact + derivation.
    run_status: RunStatus = RunStatus.MISSING_EXAMPLE
    run_checked: str | None = None  # ISO date from the results artifact, if any
    run_detail: str | None = None  # short diff / why summary for failing/awaiting
    response_model: str = ""  # route response model (wrapper-stripped) for paste/ingest
    request_model: str | None = None  # route request model, for mutation pastes


@dataclass
class EndpointClassProgress:
    """All methods in an endpoint class, grouped by path sub-root."""

    class_name: str
    display_name: str
    aliases: list[str] = field(default_factory=list)
    path_root: str = ""
    helpers: list[MethodProgress] = field(default_factory=list)
    sub_groups: dict[str, list[MethodProgress]] = field(default_factory=dict)
    total_methods: int = 0
    total_with_route: int = 0
    total_with_example: int = 0
    total_with_cli: int = 0


def classify_action_items(
    groups: list[EndpointGroup],
    fixtures: list[Fixture],
    fixture_files: set[str],
    constants: list[Constant],
) -> list[ActionItem]:
    """Classify non-done endpoints into action items with blocker types.

    Status classification logic (constitution v2.1.0):
    1. not_started AND no fixture record -> "not_implemented"
    2. pending AND path has param AND required constant missing -> "constant_needed"
    3. any non-captured fixture or missing fixture file -> "needs_request_data"
    """
    from ab.progress.instructions import build_instructions, detect_required_constants

    fixture_map: dict[tuple[str, str], Fixture] = {}
    for f in fixtures:
        fixture_map[(f.endpoint_path, f.method)] = f

    constant_names = {c.name for c in constants}
    items: list[ActionItem] = []

    # Also index fixtures by model name for done-endpoint matching
    fixture_by_model: dict[str, Fixture] = {}
    for f in fixtures:
        fixture_by_model[f.model_name] = f

    for group in groups:
        for ep in group.endpoints:
            fixture = fixture_map.get((ep.path, ep.method))
            exists = ep.response_model in fixture_files

            # Done endpoints: skip unless they have a non-captured fixture
            # without a file on disk (code exists but fixture not yet captured)
            if ep.ab_status == "done":
                if exists:
                    continue  # fully done
                # Check if there's a non-captured fixture for this model
                model_fixture = fixture_by_model.get(ep.response_model)
                if model_fixture and model_fixture.status != "captured":
                    fixture = model_fixture
                else:
                    continue  # done and no outstanding fixture record

            # Determine tier: 1 = has code (done or pending), 2 = not started
            tier = 2 if ep.ab_status == "not_started" else 1

            # Determine required constants
            req_consts = detect_required_constants(ep)
            missing = [c for c in req_consts if c not in constant_names]

            # Determine blocker type
            if ep.ab_status == "not_started" and fixture is None:
                blocker = "not_implemented"
            elif missing and ep.ab_status != "not_started":
                blocker = "constant_needed"
            elif ep.ab_status == "not_started":
                blocker = "not_implemented"
            else:
                blocker = "needs_request_data"

            item = ActionItem(
                endpoint=ep,
                tier=tier,
                fixture=fixture,
                fixture_exists=exists,
                blocker_type=blocker,
                required_constants=req_consts,
                missing_constants=missing,
            )
            item.instructions = build_instructions(item, constants)
            items.append(item)

    # Second pass: add pending fixtures not covered by any action item above.
    # This handles cases where FIXTURES.md model names differ from api-surface
    # response model names (e.g., TimelineTask vs TimelineResponse).
    covered_fixtures = {
        i.fixture.model_name for i in items if i.fixture is not None
    }
    covered_models = {i.endpoint.response_model for i in items}

    for fix in fixtures:
        if fix.status == "captured":
            continue
        if fix.model_name in covered_fixtures or fix.model_name in covered_models:
            continue
        if fix.model_name in fixture_files:
            continue  # already captured on disk

        # Create a synthetic endpoint for this orphan fixture
        ep = Endpoint(
            group_name=_group_from_path(fix.endpoint_path),
            api_surface="ACPortal",
            index=0,
            route_key="",
            method=fix.method,
            path=fix.endpoint_path,
            response_model=fix.model_name,
            ab_status="pending",
            ref_status="none",
        )

        req_consts = detect_required_constants(ep)
        missing = [c for c in req_consts if c not in constant_names]

        if missing:
            blocker = "constant_needed"
        else:
            blocker = "needs_request_data"

        item = ActionItem(
            endpoint=ep,
            tier=1,
            fixture=fix,
            fixture_exists=False,
            blocker_type=blocker,
            required_constants=req_consts,
            missing_constants=missing,
        )
        item.instructions = build_instructions(item, constants)
        items.append(item)

    return items


def _group_from_path(endpoint_path: str) -> str:
    """Infer a group name from an endpoint path."""
    parts = endpoint_path.strip("/").split("/")
    if parts:
        return parts[0].capitalize()
    return "Unknown"


