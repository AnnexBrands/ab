# Contract: Fixture Loader Interface

**Feature**: 013-test-mock-framework

## load_fixture(model_name: str) -> dict | list

**Location**: `tests/conftest.py`

### Behavior

1. Check `tests/fixtures/{model_name}.json` — if exists, load and return
2. Check `tests/fixtures/mocks/{model_name}.json` — if exists, load and return
3. Raise `FileNotFoundError` if neither exists

### Precedence

Live fixture (`tests/fixtures/`) always takes precedence over mock (`tests/fixtures/mocks/`).

### Invariants

- Return type is always `dict` or `list` (parsed JSON)
- File must contain valid JSON
- Raises `ValueError` on malformed JSON
- Callers cannot distinguish live vs mock from the return value (opaque)

---

## require_fixture(model_name, method, path, *, required) -> dict | list

**Location**: `tests/conftest.py`

### Behavior

1. Check both fixture paths (live, then mock) for existence
2. If neither exists and `required=True`: `pytest.fail()`
3. If neither exists and `required=False`: `pytest.skip()` with actionable message
4. If found: delegate to `load_fixture()`

### Change from Current

Currently only checks `tests/fixtures/`. After this feature, checks both paths with live precedence.

---

## evaluate_g2(model_name: str) -> GateResult

**Location**: `ab/progress/gates.py`

### Behavior

1. Check `tests/fixtures/{model_name}.json` — if exists, PASS (provenance: "live")
2. Check `tests/fixtures/mocks/{model_name}.json` — if exists, PASS (provenance: "mock")
3. Neither exists: FAIL

### Gate Output

- `GateResult.passed`: True if fixture found in either location
- `GateResult.message`: Includes provenance ("live fixture" or "mock fixture")
