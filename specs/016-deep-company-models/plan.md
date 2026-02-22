# Implementation Plan: Deep Pydantic Models for Company Response

**Branch**: `016-deep-company-models` | **Date**: 2026-02-22 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/016-deep-company-models/spec.md`

## Summary

Replace `dict`-typed nested fields in `CompanyDetails` with properly typed pydantic models derived from C# source entities. The `/details` and `/fulldetails` endpoints return the same combined shape (the fulldetails fixture contains both envelope sections AND flat Company entity fields), so the single `CompanyDetails` model is kept but its nested structures are typed. New models: `CompanyInfo`, `AddressData`, `OverridableField`, `OverridableAddressData`, `CompanyInsurancePricing`, `CompanyServicePricing`, `CompanyTaxPricing`.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/`)
**Testing**: pytest
**Target Platform**: Python SDK library
**Project Type**: single
**Performance Goals**: N/A (model definitions only)
**Constraints**: Backward compatibility — existing field names and aliases must remain stable
**Scale/Scope**: ~7 new nested model classes in `ab/api/models/companies.py`, fixture updates, test updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | **PASS** | This feature directly implements Principle I — replacing dict fields with validated pydantic models |
| II. Example-Driven Fixture Capture | **PASS** | Existing fixtures are already captured; models are being refined to match reality |
| III. Four-Way Harmony | **PASS** | Updated models propagate to existing endpoints, examples, fixtures, tests |
| IV. Swagger-Informed, Reality-Validated | **PASS** | Models derived from C# source (Tier 1) and validated against captured fixtures (Tier 2) |
| V. Endpoint Status Tracking | **PASS** | No new endpoints; FIXTURES.md updated if fixture structure changes |
| IX. Endpoint Input Validation | **N/A** | This feature affects response models, not request models |

No constitution violations. All gates pass.

## Project Structure

### Documentation (this feature)

```text
specs/016-deep-company-models/
├── plan.md              # This file
├── research.md          # Phase 0: C# entity research findings
├── data-model.md        # Phase 1: New pydantic model definitions
├── quickstart.md        # Phase 1: Usage examples
├── contracts/           # Phase 1: Model field contracts
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
ab/api/models/companies.py    # Add new nested models, update CompanyDetails fields
ab/api/endpoints/companies.py  # No changes expected (routes already correct)
tests/fixtures/CompanyDetails.json  # May need re-capture if fixture validation fails
tests/integration/test_companies.py  # Update assertions to test typed nested access
examples/companies.py              # Verify examples still work
```

**Structure Decision**: All changes are within the existing single-project structure. New models are added to the existing `ab/api/models/companies.py` module. No new files needed except spec artifacts.
