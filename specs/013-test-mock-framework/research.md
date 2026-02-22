# Research: Unified Test Mock Framework

**Feature**: 013-test-mock-framework
**Date**: 2026-02-21

## Decision 1: Mock Fixture Storage Strategy

**Decision**: Store mock fixtures in `tests/fixtures/mocks/` subdirectory, using the same `ModelName.json` naming convention as live fixtures.

**Rationale**: Directory-based provenance is simpler than manifest files or naming conventions. The fixture loader (`conftest.py:load_fixture`) can fall back from `tests/fixtures/` to `tests/fixtures/mocks/` with a single path check. G2 gate evaluation (`gates.py:135-143`) needs a matching update to check both paths with live precedence.

**Alternatives considered**:
- **Manifest JSON** — Adds a tracking file that must be kept in sync; more fragile than directory structure.
- **Naming convention** (`Model.mock.json`) — Would require regex parsing in fixture loader and gate evaluator; breaks existing `{model_name}.json` convention.

## Decision 2: Constitution Principle II Deviation

**Decision**: Allow manually-authored mock fixtures as a separate tier below live-captured fixtures, stored in a distinct directory. This is a justified deviation from Principle II's prohibition on fabricated fixtures.

**Rationale**: Principle II prohibits fabricated fixtures to prevent them from being treated as evidence of API behavior. The mock framework respects this intent by:
1. Storing mocks in a clearly separate `tests/fixtures/mocks/` directory
2. Live fixtures always take precedence when both exist
3. Gate evaluations can distinguish provenance by file location
4. Mocks serve model schema validation and documentation, not API behavior validation

The developer (user) manually authors all mock fixtures — no auto-generation.

**Alternatives considered**:
- **Strict compliance** (no mock fixtures at all) — Would leave 126 endpoints without any offline test coverage, 66 model tests permanently skipped, and docs requiring staging credentials.
- **Constitution amendment** — Possible but heavier-weight; the mock subdirectory approach satisfies the spirit of Principle II while enabling offline testing.

## Decision 3: Fixture Loader Fallback Mechanism

**Decision**: Modify `conftest.py:load_fixture()` to check `tests/fixtures/{model_name}.json` first, then `tests/fixtures/mocks/{model_name}.json`. Return whichever is found first (live wins). Modify `require_fixture()` to use the same fallback so that skipped tests can now execute against mock data.

**Rationale**: Minimal change to existing infrastructure. The `require_fixture()` function currently skips when no fixture exists; with fallback it will find mock fixtures and execute the test. Tests using `required=True` (previously-captured live fixtures) remain unaffected since live fixtures are checked first.

**Alternatives considered**:
- **Separate load function** (`load_mock_fixture()`) — Would require updating every test file; higher coupling.
- **Pytest fixture injection** — More complex; would need conftest changes and decorator changes in every test.

## Decision 4: Constants Consolidation Approach

**Decision**: Expand `tests/constants.py` to be the single source of truth. Update all 15 example files to import from `tests.constants` instead of defining local copies.

**Rationale**: `tests/constants.py` already exists with the right values. The 15 example files that duplicate constants (11 with `LIVE_JOB_DISPLAY_ID`, 1 with `LIVE_COMPANY_UUID`, 1 with hardcoded contact IDs) should import from this module. No new module needed.

**Alternatives considered**:
- **New shared module** (`ab/testing/constants.py`) — Over-engineering; `tests/constants.py` already serves this purpose and examples can import from it.
- **Environment variables** — Appropriate for credentials but not for stable entity IDs used in tests and docs.

## Decision 5: Xfail Resolution Strategy (32 Tests)

**Decision**: All 32 xfails are "Tier 3 conversion pending" in `test_example_params.py` — they need `params_model` classes added to Route definitions. Resolve by creating the missing params models and updating Route definitions.

**Rationale**: These are not mock-fixture-related failures. They're missing `params_model=` on Routes that have swagger-defined query parameters. The fix is to create Pydantic RequestModel subclasses for query parameters and add them to Route definitions. PR #12 already established the pattern.

**Alternatives considered**:
- **Leave as xfail** — Contradicts the spec's SC-002 commitment to triage all 32.
- **Bulk auto-generate params models from swagger** — Risky; swagger types may not match reality. Manual creation with swagger as starting reference is safer.

## Decision 6: Model-API Mismatch Resolution

**Decision**: Fix each mismatch based on root cause category:

| Category | Count | Resolution |
|----------|-------|------------|
| Missing fields in model | 5 models (CompanyDetails: 97, ContactSimple: 30, CatalogExpandedDto: 6, LotDto: 4, CompanySimple: 2) | Add missing fields to model definitions based on live fixture data |
| Wrong response type | 2 models (PropertyType: expects dict, gets int; UserRole: expects dict, gets string list) | Correct model to match actual API behavior |
| HTTP 404 errors | 3 tests (documents.list, jobs.search, jobs.search_by_details) | Investigate endpoint paths; likely staging routing issue — convert to mock-backed tests |

**Rationale**: Missing-field fixes are straightforward — the live fixtures show exactly what fields the API returns. Type mismatches require model redesign. HTTP 404s are staging environment issues that mock fixtures can work around.

**Alternatives considered**:
- **Ignore model mismatches, only fix tests** — Violates Principle I (Pydantic Model Fidelity).
- **Wait for API fixes** — The 404s may be staging-specific; mock fixtures allow progress without waiting.

## Decision 7: G2 Gate Enhancement for Mock Fixtures

**Decision**: Modify `gates.py:evaluate_g2()` to check both `tests/fixtures/{model_name}.json` and `tests/fixtures/mocks/{model_name}.json`. Report provenance (live vs mock) in gate output but count both as PASS.

**Rationale**: The spec (FR-009) requires mock fixtures to count toward G2. Distinguishing provenance in gate output satisfies FR-010 and keeps the progress report informative about which fixtures are mock vs live.

**Alternatives considered**:
- **Separate G2-mock gate** — Over-complicates the gate system; adds a 6th gate nobody asked for.
- **Don't count mocks in G2** — Contradicts FR-009 and defeats the purpose of improving fixture coverage.
