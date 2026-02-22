# Implementation Plan: Endpoint CLI

**Branch**: `014-endpoint-cli` | **Date**: 2026-02-22 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/014-endpoint-cli/spec.md`

## Summary

Add two console-script entry points (`ab` for production, `abs` for staging) that call ABConnect API endpoints directly from the terminal. Reuse the `ex` CLI's alias and prefix-matching patterns, but dispatch to real endpoint methods via runtime introspection of `ABConnectAPI`. Extract shared aliases to prevent duplication. Regenerate the progress report as baseline housekeeping.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: N/A (CLI tool — no persistence beyond existing SDK token storage)
**Testing**: pytest>=7.0 with existing conftest.py infrastructure
**Target Platform**: Developer workstation (Linux/macOS/WSL)
**Project Type**: Single project (SDK + CLI extension)
**Performance Goals**: CLI response within 5 seconds (network-bound by API latency)
**Constraints**: No new dependencies; must share aliases with `ex`; production (`ab`) must default to no env (production)
**Scale/Scope**: 23 endpoint groups, ~200+ methods, 19 aliases

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | CLI uses existing models; no model changes |
| II. Example-Driven Fixture Capture | N/A | CLI does not capture fixtures |
| III. Four-Way Harmony | PASS | New CLI artifact adds to implementation layer; examples/tests/docs are checked as part of housekeeping |
| IV. Swagger-Informed, Reality-Validated | PASS | Endpoint methods already validated; CLI is a thin wrapper |
| V. Endpoint Status Tracking | PASS | Progress report regenerated as housekeeping |
| VI. Documentation Completeness | PASS | Sphinx checked; CLI usage documented in quickstart |
| VII. Flywheel Evolution | PASS | CLI enables faster endpoint exploration, accelerating the development loop |
| VIII. Phase-Based Context Recovery | PASS | Work organized into discrete phases |
| IX. Endpoint Input Validation | PASS | CLI forwards to validated endpoint methods; params_model validation still applies |

### Post-Phase 1 Re-check

| Principle | Status | Notes |
|-----------|--------|-------|
| All | PASS | No deviations. CLI is a consumer of existing validated infrastructure. |

## Project Structure

### Documentation (this feature)

```text
specs/014-endpoint-cli/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 research decisions
├── data-model.md        # Phase 1 data model
├── quickstart.md        # Phase 1 quickstart guide
├── contracts/           # Phase 1 internal contracts
│   └── cli-dispatcher.md
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
ab/
├── cli/                 # NEW — CLI package
│   ├── __init__.py      # Exports main_prod(), main_staging()
│   ├── __main__.py      # Core dispatch logic: main(env=None)
│   ├── aliases.py       # Shared ALIASES dict (single source of truth)
│   ├── discovery.py     # Endpoint/method introspection
│   ├── parser.py        # CLI arg → Python kwargs conversion
│   └── formatter.py     # Result → stdout formatting

examples/
└── __main__.py          # MODIFIED — import ALIASES from ab.cli.aliases

pyproject.toml           # MODIFIED — add ab/abs entry points
```

**Structure Decision**: Single project structure. New `ab/cli/` package within the existing SDK. No new top-level directories. The `examples/__main__.py` modification is a one-line import change.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | — | — |

No constitution deviations required. The CLI is a pure consumer of existing validated infrastructure.

## Phases

### Phase 1: Shared Aliases + CLI Package Skeleton (FR-001, FR-002)

**Goal**: Extract aliases to shared module, create CLI package structure, register entry points.

**Files**:
- Create `ab/cli/__init__.py` — export `main_prod`, `main_staging`
- Create `ab/cli/aliases.py` — move `ALIASES` dict from `examples/__main__.py`
- Create `ab/cli/__main__.py` — skeleton `main(env=None)` with `--list` support
- Modify `examples/__main__.py` — import `ALIASES` from `ab.cli.aliases`
- Modify `pyproject.toml` — add `ab` and `abs` entry points

**Verification**: `pip install -e . && ab --list && abs --list` both show endpoint groups.

### Phase 2: Endpoint Discovery + Method Listing (FR-006, FR-009)

**Goal**: Introspect `ABConnectAPI` to enumerate endpoints and methods, support `--list` at module level.

**Files**:
- Create `ab/cli/discovery.py` — `discover_endpoints()`, `EndpointInfo`, `MethodInfo`
- Update `ab/cli/__main__.py` — wire discovery into `--list` and module-level listing

**Verification**: `ab jobs --list` shows all 31 methods with parameter signatures.

### Phase 3: Dispatch + Argument Parsing (FR-003, FR-004, FR-005)

**Goal**: Parse CLI arguments, resolve module/method, call endpoint method, print result.

**Files**:
- Create `ab/cli/parser.py` — `parse_cli_args()` with type coercion
- Create `ab/cli/formatter.py` — `format_result()` for JSON/primitive output
- Update `ab/cli/__main__.py` — full dispatch: resolve → parse → call → format → print

**Verification**: `abs addr validate --line1="12742 E Caley Av" --city=Centennial --state=CO --zip=80111` prints JSON response.

### Phase 4: Error Handling + Edge Cases (FR-008)

**Goal**: Handle auth failures, unknown endpoints, API errors, missing args gracefully.

**Files**:
- Update `ab/cli/__main__.py` — try/except wrappers for auth, API, and argument errors
- Update `ab/cli/parser.py` — `--help` support per method

**Verification**: `ab nonexistent` prints "Unknown module" with available options. Missing credentials show clear env-file guidance.

### Phase 5: Housekeeping + Verification (FR-010, SC-003, SC-004)

**Goal**: Regenerate progress report, verify tests/ruff/sphinx, ensure parity with `ex`.

**Steps**:
- Run `python scripts/generate_progress.py` and verify clean output
- Run `pytest --tb=short -q` — 232+ passed, 0 failures
- Run `ruff check .` — clean
- Run `cd docs && make html` — builds
- Run `ex --list` and `ab --list` — verify same endpoint count and aliases

**Verification**: All success criteria (SC-001 through SC-006) pass.
