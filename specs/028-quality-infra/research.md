# Research: 028 Quality Infrastructure Sprint

**Date**: 2026-03-02
**Branch**: `028-quality-infra`

## Design Decisions

### D1: Gate Baseline Data Structure

**Decision**: JSON file mapping `"{normalized_path} {METHOD}"` keys to lists of passing gate IDs.

**Rationale**: Per-endpoint-per-gate granularity (clarified in spec) requires a mapping, not a flat set. JSON is human-readable and diff-friendly. The key format matches `route_index.py`'s normalization (`{param}` → `{_}`).

**Example**:
```json
{
  "/companies/{_} GET": ["G1", "G2", "G3", "G4", "G5", "G6"],
  "/reports/sales POST": ["G1", "G2", "G5", "G6"],
  "/lookup/{_} GET": ["G2", "G5", "G6"]
}
```

**Location**: `tests/gate_baseline.json` — lives alongside the tests that consume it.

**Alternatives considered**:
- TOML: Less standard for structured data with variable-length lists.
- Python dict literal: Not consumable by non-Python tools; harder to diff.
- SQLite: Overkill for ~231 entries.

---

### D2: Baseline Update Mechanism

**Decision**: Standalone script `scripts/update_gate_baseline.py` that runs `evaluate_all_gates()` and writes the baseline.

**Rationale**: Separating update from the regression test avoids confusion. `pytest --update-baseline` would conflate test execution with baseline mutation. A standalone script:
- Can be run independently of pytest
- Has clear intent ("I'm updating the baseline")
- Can print a diff showing what changed

**Workflow**:
```bash
# After intentional changes:
python scripts/update_gate_baseline.py
# Review diff:
git diff tests/gate_baseline.json
# Commit if satisfied
```

**Alternatives considered**:
- pytest flag (`--update-gate-baseline`): Mixes test execution with side effects. Rejected.
- Make target: Too indirect. The script is the Make target's body anyway.

---

### D3: Canonical `first_or_skip` Helper Design

**Decision**: Single function in `tests/conftest.py` that handles all fixture shapes.

**Signature**:
```python
def first_or_skip(data: dict | list) -> dict:
    """Unwrap fixture to a single model-validatable dict.

    Handles: dict passthrough, list[0] extraction, empty-list skip,
    paginated {data: [...]} and {items: [...]} unwrapping.
    """
```

**Rationale**: The three competing patterns (inline isinstance, `_first_or_skip`, paginated dict unwrapping) all solve the same problem. Consolidating into conftest.py mirrors the existing `assert_no_extra_fields` pattern.

**Unwrapping order** (matches `gates.py` evaluate_g1 logic):
1. If list → extract `[0]`, skip on empty
2. If dict with `"data"` key containing list → extract `data[0]`, skip on empty
3. If dict with `"items"` key containing list → extract `items[0]`, skip on empty (only if not a real model field)
4. Otherwise → return as-is

**Note**: The `items` field ambiguity (paginated wrapper vs model property) cannot be resolved in conftest without model context. The helper should handle cases 1-2 and the simple dict passthrough. Case 3 (items) should use case-specific logic in the test when needed.

**Alternatives considered**:
- Separate functions for list and paginated: Over-engineered for the usage pattern.
- Fixture normalization at capture time: Would violate constitution ("fixtures are raw API response").

---

### D4: Gate `unwrap_fixture` Extraction

**Decision**: Extract existing inline unwrapping logic in `gates.py:evaluate_g1()` (lines 101-123) into a standalone `unwrap_fixture()` function within the same module.

**Rationale**: The gate code already has the most complete unwrapping logic including the `items` field disambiguation (checking `model_cls.model_fields`). Extracting it makes it reusable by the regression test and any future gate consumers.

**Current location**: Inline in `evaluate_g1()`, lines 101-123.
**New location**: Top-level function in `ab/progress/gates.py`.

---

### D5: Route Exemption Strategy

**Decision**: Use existing `response_model is None` as the exemption signal — no new Route field needed.

**Rationale**: Research found 48 routes with `response_model=None`. These are DELETE operations, fire-and-forget POSTs, and raw response returns. Adding a `no_response` boolean flag would be redundant — `response_model=None` already encodes the same information. Gate evaluation should exempt these from G1-G4 denominators (response-model-dependent gates). G5 and G6 (param routing and request quality) remain counted because they concern the request side.

Additionally:
- 16 routes with `response_model="bytes"` should auto-pass G1 (raw bytes, no Pydantic model) but remain in G2 (fixture can exist) and G4 (return type can be annotated as `bytes`).
- 3 routes with primitive types (`int`, `str`, `bool`) should auto-pass G1 similarly.
- 20 routes with `response_model="ServiceBaseResponse"` are real Pydantic models — no exemption.

**Denominator changes**:
- G1: 231 → ~164 (exempt 48 None + 16 bytes + 3 primitives from failing, they become N/A)
- G2: 231 → ~183 (exempt only 48 None)
- G3: 231 → ~183 (exempt only 48 None)
- G4: 231 → ~183 (exempt only 48 None)

**Alternatives considered**:
- New `no_response: bool` field on Route: Adds complexity and requires modifying frozen dataclass for no functional gain.
- `exempt_gates: list[str]` field: Over-engineered; response_model=None is the natural signal.

---

### D6: Batch Capture Script Architecture

**Decision**: `scripts/capture_missing.py` — reads FIXTURES.md for G2-FAIL endpoints, discovers matching examples, runs them, captures results.

**Workflow**:
1. Parse FIXTURES.md for all rows where G2=FAIL and response_model is not None/bytes/primitive
2. For each, locate matching example in `examples/*.py` by endpoint path
3. If example found: run it (subprocess), check for captured fixture file, report result
4. If no example: report as "needs-example"
5. Print summary: captured N, failed M, needs-example K

**Key dependency**: The `ExampleRunner` in `examples/_runner.py` already handles fixture capture. The batch script orchestrates running multiple example files.

**Alternatives considered**:
- Direct API calls from the script: Would bypass the ExampleRunner's fixture-saving logic. Rejected.
- pytest plugin: Too coupled to the test framework for what is an operational tool.

---

### D7: Test Stub Generator Architecture

**Decision**: `scripts/generate_model_tests.py` — reads all Route definitions, generates test functions for models without existing coverage.

**Output strategy**: Generate one file per endpoint module (e.g., `tests/models/test_{module}_models.py`). If the file already exists, append only missing test methods. If the file doesn't exist, create it with standard imports.

**Duplicate detection**: For each Route with a response_model, check if any existing test file contains `def test_{snake_case_model_name}(`. If found, skip.

**Generated test pattern**:
```python
def test_{model_name_snake}(self):
    data = require_fixture("{ModelName}", "{METHOD}", "{path}")
    item = first_or_skip(data)
    model = {ModelName}.model_validate(item)
    assert isinstance(model, {ModelName})
    assert_no_extra_fields(model)
```

**Alternatives considered**:
- Jinja templates: Overhead for a simple pattern. String formatting is sufficient.
- AST manipulation of existing files: Fragile. Appending or creating new test classes is safer.

---

### D8: Return Type Annotation Approach

**Decision**: Manual sweep guided by a script that identifies mismatches, not an auto-fixer.

**Rationale**: Research found 46 methods with `-> Any`. Some of these are intentional (e.g., `documents.upload` bypasses Route entirely). An auto-fixer might incorrectly type these. A report script lists each mismatch; a developer reviews and applies fixes.

**Script**: `scripts/audit_return_types.py` — reads Route definitions, compares `response_model` against method return type annotation, outputs a CSV/table of mismatches.

**Alternatives considered**:
- Fully automated fixer: Risk of incorrect types for edge cases (bytes, None, bypass). Rejected.
- Manual-only: Tedious for 46 methods without a guide. The audit script is the middle ground.

---

## Current State Assessment

### Test Suite (from pr-analysis, verified by research)

| Metric | Value |
|--------|-------|
| Passed | 529 |
| Skipped | 54 |
| Failed | 7 |
| xfailed | 5 |

### 7 Pre-Existing Failures

| # | Test | Root Cause | Fix Approach |
|---|------|-----------|--------------|
| 1 | `test_list_users` | Positional arg after keyword-only refactor | Change `api.users.list(data)` → `api.users.list(data=data)` |
| 2 | `test_search_contact_entity_result` | Undeclared extra fields in model | Expand model fields from fixture |
| 3 | `test_response_field_values` | Same SearchContactEntityResult gap | Same fix as #2 |
| 4 | `test_priced_freight_provider` | Empty `[]` fixture, test expects dict | Use `first_or_skip` helper |
| 5 | `test_user_role` | Missing `UserRole.json` (API returns `List[str]`) | Rewrite test for string list |
| 6 | `test_all_fixture_files_tracked` | 62 fixtures on disk not in FIXTURES.md | Fix mock_coverage scanning |
| 7 | `test_captured_fixtures_exist_on_disk` | Request fixtures in `requests/` subdir not scanned | Fix mock_coverage to scan `requests/` |

### Gate Status (current)

| Gate | Pass | Total | Gap |
|------|------|-------|-----|
| G1 | 85 | 231 | 146 |
| G2 | 106 | 231 | 125 |
| G3 | 135 | 231 | 96 |
| G4 | 153 | 231 | 78 |
| G5 | 216 | 231 | 15 |
| G6 | 223 | 231 | 8 |
| All pass | 69 | 231 | 162 |

### Fixture Inventory

| Directory | Count | Purpose |
|-----------|-------|---------|
| `tests/fixtures/` | 63 | Response fixtures (live captures) |
| `tests/fixtures/mocks/` | 2 | Mock response fixtures |
| `tests/fixtures/requests/` | 115 | Request body fixtures |

### Endpoint Return Type Status

| Annotation | Count | Percentage |
|-----------|-------|-----------|
| Properly typed | 191 | 78.9% |
| `-> Any` | 46 | 19.0% |
| `-> None` | 5 | 2.1% |

### Route response_model Distribution

| Category | Count | Gate Treatment |
|----------|-------|---------------|
| Pydantic model (single) | 77 | Normal evaluation |
| `List[Model]` | 63 | Normal evaluation |
| `ServiceBaseResponse` | 20 | Normal evaluation |
| `None` (void) | 48 | Exempt from G1-G4 |
| `bytes` | 16 | Auto-pass G1 |
| Primitive (`int`, `str`, `bool`) | 3 | Auto-pass G1 |
