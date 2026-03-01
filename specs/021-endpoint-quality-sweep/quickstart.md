# Per-Endpoint Quality Checklist

Repeatable workflow for sweeping an endpoint to "complete" status across all 6 quality gates.

## Prerequisites

- Live staging API access (for fixture capture if needed)
- C# server source available at `/src/ABConnect/` (Tier 1 ground truth)
- Existing fixture in `tests/fixtures/` (or ability to capture one)

## The Checklist

### 1. Research (5 min)

- [ ] Find the C# controller action for the endpoint
- [ ] Find the C# DTO/entity class for the response
- [ ] Map every C# property to its type and nullability
- [ ] Compare fixture JSON keys against C# properties — confirm 1:1 correspondence
- [ ] Check for nested types that need typed sub-models

### 2. Model (G1 — Model Fidelity)

- [ ] Add all missing fields to the Pydantic model with correct types
- [ ] Use `Optional[T]` for nullable C# properties
- [ ] Set `alias="camelCase"` matching the JSON key for non-trivial names
- [ ] Add `Field(description="...")` for every new field
- [ ] Create typed sub-models for nested objects (reuse existing models where possible)
- [ ] Run: `python -c "from ab.api.models.contacts import ContactDetailedInfo; import json; d = json.load(open('tests/fixtures/ContactDetailedInfo.json')); m = ContactDetailedInfo.model_validate(d); print(len(m.__pydantic_extra__ or {}), 'extra fields')"` — must print `0 extra fields`

### 3. Fixture (G2 — Fixture Status)

- [ ] Confirm fixture file exists: `tests/fixtures/{ModelName}.json`
- [ ] If missing: run the example script to capture from staging
- [ ] Verify fixture is from a real API call (not fabricated)

### 4. Tests (G3 — Test Quality)

- [ ] Model test: `assert_no_extra_fields(model)` is **not** commented out
- [ ] Model test: `isinstance(model, ModelName)` assertion present
- [ ] Integration test: both `isinstance` and `assert_no_extra_fields` present
- [ ] Run: `pytest tests/models/test_contact_models.py -x -q -m "not live"` — passes
- [ ] Run: `pytest tests/ -x -q -m "not live"` — no regressions

### 5. Documentation (G4 — Doc Accuracy)

- [ ] Endpoint method has typed return annotation (not `Any`)
- [ ] Endpoint method has docstring with description
- [ ] `docs/api/{module}.md` has entry for this endpoint with example code
- [ ] Example code in docs uses model fields that actually exist

### 6. Parameter Routing (G5 — Param Routing)

- [ ] If endpoint uses query params: Route has `params_model="..."` set
- [ ] Params model declares all swagger query parameters
- [ ] If no query params: auto-pass — nothing to do

### 7. Request Quality (G6 — Request Quality)

- [ ] If endpoint has request body: method signature is typed (not `**kwargs`)
- [ ] Request model fields all have `Field(description="...")`
- [ ] No `# TODO: verify optionality` markers remain
- [ ] If no request body: auto-pass — nothing to do

### 8. Verify & Regenerate

- [ ] Run: `python scripts/generate_progress.py --fixtures` — endpoint shows all PASS
- [ ] Run: `python scripts/generate_progress.py` — HTML report updated
- [ ] Spot-check FIXTURES.md: endpoint status = "complete"

## Priority Order for Sweeping

When choosing the next endpoint to sweep, prioritize by ROI:

1. **G1-only failures** (model incomplete, fixture exists) — fastest fix, highest count
2. **G1+G3 failures** (model incomplete + tests need uncomment) — fix model, uncomment test
3. **G3-only failures** (model ok, test assertion missing) — just uncomment
4. **G4-only failures** (missing docs/type annotations) — add docstring/types
5. **G1+G2 failures** (no fixture at all) — requires live API access to capture
6. **Multi-gate failures** (new/untested endpoints) — full DISCOVER workflow needed
