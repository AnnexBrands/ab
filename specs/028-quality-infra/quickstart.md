# Quickstart: 028 Quality Infrastructure Sprint

**Branch**: `028-quality-infra`

## Prerequisites

- Python 3.11+
- Existing SDK installed (`pip install -e .`)
- `tests/` and `ab/progress/` modules available
- Staging API credentials (for batch capture only, not for other stories)

## Implementation Order

The stories have dependencies:

```
US2 (unified fixture handling) ──┐
                                 ├──> US3 (fix failures) ──> US4 (FIXTURES.md) ──> US1 (ratchet)
US7 (return types) ──────────────┘
US8 (exemptions) ─────────────────────────────────────────────────────────────────────────────>
US5 (batch capture) — independent, needs staging API
US6 (test stubs) — independent, runs after US2
```

**Recommended execution order**:
1. US2: Unified fixture handling (creates helpers needed by US3)
2. US3: Fix pre-existing failures (creates clean suite for US1)
3. US4: FIXTURES.md integrity (fixes failures #6 and #7)
4. US7: Return type sweep (mechanical, independent)
5. US8: No-response exemptions (adjusts denominators)
6. US1: Gate regression ratchet (requires clean suite + correct gates)
7. US6: Test stub generator (uses helpers from US2)
8. US5: Batch capture (requires staging API, run last)

## Quick Verification Commands

```bash
# After US2: Verify single helper definition
grep -rn "def first_or_skip\|def _first_or_skip" tests/

# After US3: Verify zero failures
cd src && pytest --tb=line -q

# After US4: Verify FIXTURES.md integrity
cd src && pytest tests/test_mock_coverage.py -v

# After US1: Verify ratchet works
cd src && pytest tests/test_gate_regression.py -v

# After US7: Check G4 improvement
cd src && python scripts/generate_progress.py --fixtures | grep "G4"

# After US6: Run generated stubs
cd src && pytest tests/models/ -v --tb=line

# After US5: Check G2 improvement
cd src && python scripts/generate_progress.py --fixtures | grep "G2"
```

## Key Files to Modify

| Story | Files Modified | Files Created |
|-------|---------------|--------------|
| US1 | — | `tests/test_gate_regression.py`, `scripts/update_gate_baseline.py`, `tests/gate_baseline.json` |
| US2 | `tests/conftest.py`, `tests/models/test_report_models.py`, `tests/models/test_extended_lookup_models.py`, `tests/models/test_lookup_models.py`, `tests/models/test_shipment_models.py`, `ab/progress/gates.py` | — |
| US3 | `tests/integration/test_users.py` or `tests/models/test_user_models.py`, `tests/models/test_freight_models.py`, `ab/api/models/contacts.py` | — |
| US4 | `tests/test_mock_coverage.py`, `FIXTURES.md` (regenerated) | — |
| US5 | — | `scripts/capture_missing.py` |
| US6 | — | `scripts/generate_model_tests.py`, `tests/models/test_*_models.py` (generated stubs) |
| US7 | `ab/api/endpoints/*.py` (11 files with `-> Any`) | `scripts/audit_return_types.py` |
| US8 | `ab/progress/gates.py` (exemption logic) | — |

## Success Verification

After all stories complete:
```bash
# Zero failures
cd src && pytest --tb=line -q
# Gate ratchet protects gains
cd src && pytest tests/test_gate_regression.py -v
# FIXTURES.md is accurate
cd src && pytest tests/test_mock_coverage.py -v
# Progress report shows improvement
cd src && python scripts/generate_progress.py --fixtures
# Expected: All-pass count >= 130, G4 >= 200
```
