# Implementation Plan: Client Endpoint Type Hints

**Branch**: `032-client-type-hints` | **Date**: 2026-03-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/032-client-type-hints/spec.md`

## Summary

Add explicit type annotations to all 22 endpoint attributes and 2 backward-compatible aliases on `ABConnectAPI` in `ab/client.py`. This is a purely additive change — no behavioral modifications. The type hints enable IDE autocompletion (Ctrl+Space) on `api.<endpoint>.` and full signature/model discoverability. Sphinx docs, CLI `--list`/`--help`, and examples must be verified unchanged.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: N/A — SDK, no local storage
**Testing**: pytest (existing test suite)
**Target Platform**: Python SDK (cross-platform)
**Project Type**: Single project (Python SDK)
**Performance Goals**: N/A — compile-time/static-analysis change only
**Constraints**: Zero runtime behavior change; zero new dependencies
**Scale/Scope**: 1 file modified (`ab/client.py`), verification across docs/CLI/tests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | No model changes. Endpoint types already use Pydantic models. |
| II. Example-Driven Fixture Capture | PASS | No fixture changes. Examples unchanged. |
| III. Four-Way Harmony | PASS | Type hints are additive metadata — all four artifacts (impl, example, fixture/test, docs) remain consistent. Sphinx autodoc benefits from the annotations. |
| IV. Swagger-Informed, Reality-Validated | PASS | No swagger or model changes. |
| V. Endpoint Status Tracking | PASS | No endpoint additions or removals. |
| VI. Documentation Completeness | PASS | Sphinx autodoc will pick up the type annotations automatically. Verify build. |
| VII. Flywheel Evolution | PASS | This feature directly addresses developer experience feedback (IDE discoverability). |
| VIII. Phase-Based Context Recovery | PASS | Single-file change, easy to checkpoint. |
| IX. Endpoint Input Validation | PASS | No changes to endpoint methods or request handling. |

**Gate result**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/032-client-type-hints/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
ab/
├── client.py            # PRIMARY CHANGE — add type annotations to endpoint attributes
├── api/
│   ├── endpoints/
│   │   ├── __init__.py  # Already exports all endpoint classes (no change needed)
│   │   ├── dashboard.py
│   │   ├── companies.py
│   │   └── ...          # 22 endpoint modules total
│   └── models/
│       └── ...          # Pydantic models (no changes)
├── cli/
│   ├── __init__.py      # CLI entry points (verify unchanged output)
│   └── __main__.py      # CLI dispatcher (verify --list, --help)
docs/
├── conf.py              # Sphinx config (verify build)
├── api/                 # Endpoint docs (verify autodoc picks up types)
└── models/              # Model docs (no changes)
examples/
└── ...                  # 30+ example modules (verify still run)
tests/
└── unit/                # Unit tests (verify all pass)
```

**Structure Decision**: Single project layout. Only `ab/client.py` is modified. All other paths are verification targets.
