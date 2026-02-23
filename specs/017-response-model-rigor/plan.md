# Implementation Plan: Response Model Rigor

**Branch**: `017-response-model-rigor` | **Date**: 2026-02-22 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/017-response-model-rigor/spec.md`

## Summary

Fix a silent correctness bug where `BaseEndpoint._request` returns raw dicts when the API wraps list responses in wrapper objects. Add mandatory `fixture_file` to all example entries with `response_model`. Add a test gate enforcing fixture completeness. Clean up stale `progress.html`.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/`)
**Testing**: pytest (existing test suite, 307+ passed baseline)
**Target Platform**: Python SDK (library)
**Project Type**: Single project
**Performance Goals**: N/A (SDK correctness fix)
**Constraints**: No breaking changes to public API; test count must not decrease
**Scale/Scope**: ~4 files modified, ~46 example entries updated, 1 new test file

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | VIOLATION (being fixed) | `_request` line 97 returns raw dict — this feature fixes it |
| II. Example-Driven Fixture Capture | VIOLATION (being fixed) | 46 entries have response_model without fixture_file |
| III. Four-Way Harmony | PARTIAL | Fixtures missing for 46 endpoints means harmony is broken |
| IV. Swagger-Informed, Reality-Validated | OK | Swagger says bare arrays; reality has wrappers — fix handles reality |
| V. Endpoint Status Tracking | OK | FIXTURES.md exists and is maintained |
| VI. Documentation Completeness | N/A | No new endpoints |
| VII. Flywheel Evolution | OK | This feature itself is a flywheel output |
| VIII. Phase-Based Context Recovery | OK | Tasks will use checkbox format |
| IX. Endpoint Input Validation | N/A | No input changes |

**Gate result**: PASS — violations are the purpose of this feature.

## Project Structure

### Documentation (this feature)

```text
specs/017-response-model-rigor/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── list-unwrap.md
│   └── fixture-completeness.md
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
ab/
├── api/
│   └── base.py                          # Fix _request list-unwrap logic
examples/
├── _runner.py                           # (no changes expected)
├── parcels.py                           # Add fixture_file entries
├── jobs.py                              # Add fixture_file entries
├── companies.py                         # Add fixture_file entries
├── shipments.py                         # Add fixture_file entries
├── rfq.py                               # Add fixture_file entries
├── views.py                             # Add fixture_file entries
├── commodities.py                       # Add fixture_file entries
├── partners.py                          # Add fixture_file entries
├── contacts.py                          # Add fixture_file entries
├── catalog.py                           # Add fixture_file entries
├── lots.py                              # Add fixture_file entries
├── reports.py                           # Add fixture_file entries
├── lookup_extended.py                   # Add fixture_file entries
├── tracking.py                          # Add fixture_file entries
├── autoprice.py                         # Add fixture_file entries
└── web2lead.py                          # Add fixture_file entries

tests/
├── test_fixture_completeness.py         # New: gate test for fixture_file presence
└── models/
    └── test_parcel_models.py            # Existing (may need array fixture handling)

progress.html                            # DELETE (moved to html/)
```

**Structure Decision**: Existing SDK structure. No new directories. One new test file for the fixture completeness gate. All other changes are modifications to existing files.
