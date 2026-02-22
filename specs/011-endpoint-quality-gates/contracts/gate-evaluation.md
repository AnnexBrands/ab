# Contract: Gate Evaluation Functions

**Date**: 2026-02-21

## Gate G1: Model Fidelity

**Input**: model_name (str), fixture_path (str)
**Output**: GateResult(passed: bool, reason: str)

**Algorithm**:
1. Import model class from `ab.api.models`
2. Load fixture JSON from `tests/fixtures/{model_name}.json`
3. Call `model_cls.model_validate(fixture_data)`
4. Check `model.__pydantic_extra__`
5. If empty → pass
6. If non-empty → fail with list of undeclared field names

**Edge cases**:
- Model class not found → fail("Model class not found in ab.api.models")
- Fixture is a list → validate first element
- Fixture is a paginated wrapper → validate `data[0]` or `items[0]`

## Gate G2: Fixture Status

**Input**: model_name (str)
**Output**: GateResult(passed: bool, reason: str)

**Algorithm**:
1. Check if `tests/fixtures/{model_name}.json` exists on disk
2. If exists → pass
3. If not → fail("Fixture file not found")

**Note**: This gate does NOT re-validate that the fixture was captured from a real API. That is enforced by process (Constitution Principle II) not by code.

## Gate G3: Test Quality

**Input**: endpoint_path (str), method (str), model_name (str)
**Output**: GateResult(passed: bool, reason: str)

**Algorithm** (static analysis of test files):
1. Scan `tests/integration/` for test methods that call the endpoint
2. Check for `isinstance(result, {ModelClass})` assertion
3. Check for `__pydantic_extra__` assertion
4. Scan `tests/models/` for fixture validation test for this model
5. Check for `__pydantic_extra__` assertion in fixture test
6. Both must exist and have substantive assertions → pass

## Gate G4: Documentation Accuracy

**Input**: endpoint_module (str), method_name (str), model_name (str)
**Output**: GateResult(passed: bool, reason: str)

**Algorithm**:
1. Read the endpoint method's `-> X` return type annotation
2. If `-> Any` → fail("Return type is Any, should be {model_name}")
3. Check `docs/api/{service}.md` for correct `{class}` reference
4. Check `docs/models/{service}.md` exists with automodule directive
5. All checks pass → pass

## FIXTURES.md Generation

**Input**: All gate results for all endpoints
**Output**: Regenerated FIXTURES.md

**Algorithm**:
1. Parse existing FIXTURES.md to extract Notes column
2. Evaluate all gates for all endpoints
3. Generate markdown table with columns: Path, Method, Req Model, Resp Model, G1, G2, G3, G4, Status, Notes
4. Status = "complete" only if all applicable gates pass
5. Preserve hand-maintained Notes from existing file
6. Write to FIXTURES.md

## progress.html Generation

**Input**: All gate results, endpoint definitions, fixture inventory
**Output**: HTML dashboard

**Algorithm**:
1. Evaluate all gates
2. Compute summary stats (total, per-gate pass counts, overall complete)
3. Group by API surface and endpoint group
4. Render HTML table with per-gate pass/fail badges
5. Include summary cards at top
