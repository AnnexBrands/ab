# Data Model: 028 Quality Infrastructure Sprint

**Date**: 2026-03-02
**Branch**: `028-quality-infra`

## Entities

### Gate Baseline (`tests/gate_baseline.json`)

Per-endpoint-per-gate record of passing gates. One-directional ratchet — gates can only be added, never removed (except via explicit baseline update).

**Schema**:
```
{
  "<normalized_path> <METHOD>": ["G1", "G2", ...],
  ...
}
```

**Key**: `"{normalized_path} {METHOD}"` — path with `{param}` → `{_}` normalization, matching `route_index.py:normalize_path()`. Example: `"/companies/{_} GET"`.

**Value**: Sorted list of gate IDs (subset of `["G1", "G2", "G3", "G4", "G5", "G6"]`) that this endpoint currently passes.

**Constraints**:
- Keys must correspond to real Route definitions (validated on load)
- Values must be a subset of the 6 defined gates
- File is deterministically sorted by key for stable diffs

**Lifecycle**:
1. **Created**: `scripts/update_gate_baseline.py` runs `evaluate_all_gates()`, writes baseline
2. **Consumed**: `tests/test_gate_regression.py` loads baseline, runs `evaluate_all_gates()`, asserts no regressions
3. **Updated**: Developer re-runs update script after intentional changes, commits new baseline

---

### Route (existing — `ab/api/route.py`)

Frozen dataclass defining an API endpoint. **No modifications needed** (D5).

**Relevant fields for this feature**:
- `response_model: Optional[str]` — `None` signals void/no-response endpoint → exempt from G1-G4
- `request_model: Optional[str]` — Used by test stub generator
- `params_model: Optional[str]` — Used by G5 evaluation
- `method: str` — HTTP method
- `path: str` — Endpoint path with `{param}` placeholders

---

### EndpointGateStatus (existing — `ab/progress/gates.py`)

Return type of `evaluate_all_gates()`. One per endpoint.

**Fields**:
- `endpoint_path: str`
- `method: str`
- `gates: dict[str, GateResult]` — G1-G6 results

**GateResult fields**:
- `gate_id: str` — e.g., "G1"
- `passed: bool`
- `reason: str` — Human-readable explanation

---

### Batch Capture Summary (new — stdout output)

Output of `scripts/capture_missing.py`. Not persisted to file.

**Fields**:
- `total: int` — Endpoints processed
- `captured: int` — Successfully captured fixtures
- `failed: int` — Example ran but returned error
- `needs_example: int` — No example file found
- `details: list[CaptureResult]` — Per-endpoint results

**CaptureResult**:
- `path: str` — Endpoint path
- `method: str` — HTTP method
- `status: str` — "captured" | "failed" | "needs-example"
- `message: str` — Detail (e.g., "HTTP 500", "No example in examples/reports.py")

## Relationships

```
Route ──defines──> EndpointGateStatus (via evaluate_all_gates)
EndpointGateStatus ──serializes──> Gate Baseline JSON
Gate Baseline JSON ──consumed by──> test_gate_regression.py
FIXTURES.md ──consumed by──> test_mock_coverage.py
FIXTURES.md ──consumed by──> capture_missing.py (batch capture)
Route definitions ──consumed by──> generate_model_tests.py (test stubs)
```

## State Transitions

### Gate Baseline Lifecycle

```
[not exists] ──create──> [baseline v1]
[baseline v1] ──regression detected──> test FAILS (baseline unchanged)
[baseline v1] ──intentional change + update──> [baseline v2]
[baseline v2] ──new gates pass + update──> [baseline v3] (ratchet forward)
```

### Fixture Status Lifecycle (per endpoint)

```
[G2=FAIL] ──batch capture succeeds──> [G2=PASS]
[G2=FAIL] ──batch capture fails──> [G2=FAIL] (error logged)
[G2=FAIL] ──no example exists──> [G2=FAIL] (needs-example logged)
```
