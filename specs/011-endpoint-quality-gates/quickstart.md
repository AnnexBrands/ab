# Quickstart: Endpoint Quality Gates

**Date**: 2026-02-21
**Feature**: 011-endpoint-quality-gates

## What This Feature Does

Establishes multi-dimensional quality gates for every SDK endpoint and enforces honest status tracking. An endpoint is only "complete" when it passes all four gates:

1. **G1 — Model Fidelity**: Response model declares all API fields (zero `__pydantic_extra__`)
2. **G2 — Fixture Status**: Fixture file captured from real API exists
3. **G3 — Test Quality**: Tests assert `isinstance` + zero extra fields
4. **G4 — Doc Accuracy**: Sphinx docs show correct return type

## Implementation Order

### Phase 1: Gate Infrastructure
- Create gate evaluation functions in `ab/progress/gates.py`
- Add `__pydantic_extra__` assertion helpers to `tests/conftest.py`

### Phase 2: Model Updates (15 models, ~30 sub-models)
- Add missing fields to all 15 models in the Warning Summary
- Create full-depth typed sub-models (CompanyAddress, CompanyPricing, etc.)
- Register new models in `ab/api/models/__init__.py`

### Phase 3: Test Hardening
- Rewrite integration tests: `isinstance` + `__pydantic_extra__` checks
- Rewrite fixture-validation tests: `__pydantic_extra__` assertions
- Verify all tests pass with updated models

### Phase 4: Documentation Fixes
- Add return type annotations to all endpoint methods (replace `-> Any`)
- Verify Sphinx docs show correct types
- Ensure model autodoc pages include new sub-models

### Phase 5: Progress & Status Generation
- Extend `ab.progress` module with gate evaluation
- Implement FIXTURES.md generation from source artifacts
- Implement progress.html with per-gate columns
- Generate initial baseline (most gates failing — expected)

## Running the Gates

```bash
# Run fixture validation tests (G1 + G3)
pytest tests/models/ -v

# Run integration tests (G3)
pytest tests/integration/ -v

# Generate FIXTURES.md and progress.html (G1 + G2 + G3 + G4)
python scripts/generate_progress.py

# Build docs and check for warnings (G4)
cd docs && make html
```

## Key Files Modified

| File | Change |
|------|--------|
| `ab/api/models/companies.py` | Add missing fields + ~20 sub-models |
| `ab/api/models/contacts.py` | Add missing fields |
| `ab/api/models/shipments.py` | Add missing fields + Weight sub-model |
| `ab/api/models/jobs.py` | Add notedConditions to CalendarItem |
| `ab/api/models/lookup.py` | Add value, id, iataCode fields |
| `ab/api/models/users.py` | Add 18+ missing fields |
| `ab/api/models/forms.py` | Add 11 missing fields |
| `ab/api/models/sellers.py` | Add customerDisplayId, isActive |
| `ab/api/models/web2lead.py` | Add SubmitNewLeadPOSTResult alias |
| `ab/api/models/address.py` | Add 6 missing fields |
| `ab/api/models/common.py` | NEW — shared sub-models (Coordinates, Address) |
| `ab/api/models/__init__.py` | Register all new models |
| `ab/api/endpoints/*.py` | Replace `-> Any` with actual types |
| `tests/integration/*.py` | Substantive assertions |
| `tests/models/*.py` | `__pydantic_extra__` assertions |
| `ab/progress/gates.py` | NEW — gate evaluation functions |
| `scripts/generate_progress.py` | Extended with gate evaluation |
| `FIXTURES.md` | Regenerated with per-gate columns |
| `docs/models/*.md` | Updated for new sub-models |
