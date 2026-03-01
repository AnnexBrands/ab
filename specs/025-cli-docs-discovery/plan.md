# Implementation Plan: CLI Docs & Discovery Major Release

**Branch**: `025-cli-docs-discovery` | **Date**: 2026-03-01 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/025-cli-docs-discovery/spec.md`

## Summary

Enrich the CLI (`ab`/`abs`), ExampleRunner (`ex`), progress reporting, and Sphinx documentation with Route-derived metadata. The Route dataclass is already the single source of truth for endpoint URI, HTTP method, request/response models, and params model. This feature threads that metadata through the CLI help system, the example runner's auto-discovery, the progress HTML report, and Sphinx autodoc — creating a unified, self-documenting developer experience without adding any new metadata storage.

**Technical approach**: Source-code introspection maps each endpoint method to its Route constant. A new `RouteResolver` module parses method bodies to find `self._request(_ROUTE_NAME...)` calls, producing a `method_name → Route` lookup per endpoint class. This lookup feeds enriched `MethodInfo` dataclasses that the CLI, ExampleRunner, and progress system consume.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests, sphinx, sphinx-rtd-theme, myst-parser (all existing — no new dependencies)
**Storage**: Filesystem (HTML reports in `html/`, fixture JSON in `tests/fixtures/`)
**Testing**: pytest (existing — unit tests for resolver logic, integration tests for CLI output)
**Target Platform**: CLI tool (Linux/macOS/Windows terminal)
**Project Type**: Single project (existing SDK structure)
**Performance Goals**: CLI `--help` and `--list` must complete in <500ms without credentials. Progress report generation must complete in <10s for all endpoints.
**Constraints**: No API calls for help/listing. Route introspection must work without instantiating the API client. No new dependencies.
**Scale/Scope**: ~220 ACPortal endpoints, ~15 endpoint classes, ~200 methods, 6 user stories

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | No new API models. Internal dataclasses (`MethodInfo`, `EndpointProgress`) are plain Python dataclasses, not Pydantic API models. Route metadata is consumed read-only. |
| II. Example-Driven Fixture Capture | PASS (enhanced) | FR-006/007 strengthen this principle by auto-discovering `response_model` and `fixture_file` from Routes, reducing manual duplication. |
| III. Four-Way Harmony | PASS (enhanced) | This feature directly strengthens all four artifacts by making Route metadata visible in CLI help, Sphinx docs, and progress tracking. The shared alias registry (FR-013) ensures naming consistency across all four. |
| IV. Swagger-Informed, Reality-Validated | PASS | No change to swagger validation. Route remains the authoritative source. |
| V. Endpoint Status Tracking | PASS (enhanced) | FR-008–011 upgrade the progress report with richer grouping, dotted paths, and ex/ab status columns. |
| VI. Documentation Completeness | PASS (enhanced) | FR-016/017 formalize structured docstrings and auto-generated Sphinx pages. CLI help and Sphinx show identical factual content. |
| VII. Flywheel Evolution | PASS | This feature is a direct result of stakeholder input → showcase cycle. The enriched CLI and progress report feed the next flywheel rotation. |
| VIII. Phase-Based Context Recovery | PASS | Implementation will follow phased commits. Each user story delivers independently testable artifacts. |
| IX. Endpoint Input Validation | PASS | No change to input validation. Route-based discovery is read-only introspection. |

**Gate result: ALL PASS. No violations. Proceed to Phase 0.**

## Project Structure

### Documentation (this feature)

```text
specs/025-cli-docs-discovery/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── cli-help-format.md
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
ab/cli/
├── __main__.py          # MODIFY: implicit listing, enriched output
├── aliases.py           # UNCHANGED: already shared across ab/ex
├── discovery.py         # MODIFY: extend MethodInfo with Route metadata
├── formatter.py         # UNCHANGED
├── parser.py            # MODIFY: rich --help output with URI, signature, models
└── route_resolver.py    # NEW: maps endpoint methods → Route constants

ab/progress/
├── models.py            # MODIFY: add EndpointProgress dataclass
├── renderer.py          # MODIFY: grouped view with dotted paths, ex/ab columns
├── fixtures_generator.py # MODIFY: include dotted paths in FIXTURES.md
├── gates.py             # UNCHANGED
├── route_index.py       # MODIFY: add method→route mapping for dotted paths
└── instructions.py      # MODIFY: generic constant discovery via path_param_to_constant()

examples/
├── _runner.py           # MODIFY: auto-discover models from Routes
└── __main__.py          # UNCHANGED

docs/
├── conf.py              # UNCHANGED (or minor autodoc tweaks)
└── api/                 # MODIFY: structured method reference pages

scripts/
└── generate_progress.py # MODIFY: pass new data to renderer

tests/
├── unit/
│   └── test_route_resolver.py  # NEW: unit tests for resolver
└── integration/
    └── test_cli_output.py      # NEW: verify CLI help/listing format
```

**Structure Decision**: Single project. All changes extend existing modules in `ab/cli/`, `ab/progress/`, `examples/`, and `docs/`. One new module (`ab/cli/route_resolver.py`) encapsulates the Route-to-method matching logic. No new packages or project-level structure changes.

## Complexity Tracking

> No constitution violations. No complexity justifications needed.
