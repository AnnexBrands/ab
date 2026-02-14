# Implementation Plan: Scaffold Examples & Fixtures

**Branch**: `004-scaffold-examples-fixtures` | **Date**: 2026-02-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-scaffold-examples-fixtures/spec.md`

## Summary

Transform the 16 flat example scripts into structured, runner-wrapped example files that serve as both SDK documentation and automated fixture-capture tools. Create 3 missing example files (address, lookup, users), expand 2 incomplete files (jobs, lots), and build a shared runner module that handles API calls, model validation, JSON serialization, and fixture saving. Every public endpoint method gets a structured entry with declared metadata (request params, request/response model names, fixture file path).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/`)
**Testing**: pytest (existing infrastructure, no new test framework)
**Target Platform**: Developer workstation with staging API credentials
**Project Type**: Single Python package
**Performance Goals**: N/A — developer tooling, not production runtime
**Constraints**: Must not break existing test infrastructure (fixture loading, `require_fixture()`, model validation tests)
**Scale/Scope**: 15 endpoint modules → 15 example files + 1 runner module + 1 package init

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | Runner uses existing models via `model_dump(by_alias=True, mode="json")`. No new models needed. |
| II. Example-Driven Fixture Capture | PASS — **Primary alignment** | This feature IS the implementation of Principle II. Runner automates the capture loop described in the constitution. |
| III. Four-Way Harmony | PASS | Examples are artifact #2 of the four-way harmony. This feature ensures every endpoint has one. Fixtures (#3) are captured by running examples. |
| IV. Swagger-Informed, Reality-Validated | PASS | Fixture capture uses real API responses, not swagger-derived data. |
| V. Endpoint Status Tracking | PASS | TODO annotations in examples cross-reference FIXTURES.md status. Runner does not auto-update FIXTURES.md (manual tracking preserved). |
| VI. Documentation Completeness | N/A | Sphinx docs are not in scope for this feature. |
| VII. Flywheel Evolution | PASS | This feature is the output of a flywheel rotation: stakeholder need (fixture gaps) → engineering work (runner infrastructure). |
| VIII. Phase-Based Context Recovery | PASS | Plan follows DISCOVER phases. Each migration batch produces committed checkpoint artifacts. |

**Gate result**: PASS — no violations. Complexity tracking not needed.

## Project Structure

### Documentation (this feature)

```text
specs/004-scaffold-examples-fixtures/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 research decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Usage guide for new example pattern
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
examples/
├── __init__.py          # NEW — package marker (enables python -m execution)
├── _runner.py           # NEW — ExampleRunner class + ExampleEntry + fixture save
├── address.py           # NEW — structured entries for AddressEndpoint (2 methods)
├── lookup.py            # NEW — structured entries for LookupEndpoint (4 methods)
├── users.py             # NEW — structured entries for UsersEndpoint (4 methods)
├── autoprice.py         # MIGRATE — wrap in runner (2 methods)
├── catalog.py           # MIGRATE — wrap in runner (catalog methods)
├── companies.py         # MIGRATE — wrap in runner (8 methods)
├── contacts.py          # MIGRATE — wrap in runner (contact methods)
├── documents.py         # MIGRATE — wrap in runner (document methods)
├── forms.py             # MIGRATE — wrap in runner (15 methods)
├── jobs.py              # MIGRATE + EXPAND — 2 → 28+ methods
├── lots.py              # MIGRATE + EXPAND — 1 → all lot methods
├── notes.py             # MIGRATE — wrap in runner (note methods)
├── parcels.py           # MIGRATE — wrap in runner (parcel methods)
├── payments.py          # MIGRATE — wrap in runner (payment methods)
├── sellers.py           # MIGRATE — wrap in runner (seller methods)
├── shipments.py         # MIGRATE — wrap in runner (14 methods)
├── timeline.py          # MIGRATE — wrap in runner (timeline methods)
├── tracking.py          # MIGRATE — wrap in runner (tracking methods)
└── web2lead.py          # MIGRATE — wrap in runner (web2lead methods)
```

**Structure Decision**: No new directories beyond adding `examples/__init__.py`. The runner module lives inside `examples/` as `_runner.py` (underscore prefix = infrastructure, not a user-facing example). All existing files are modified in place. Tests directory unchanged.

## Implementation Phases

### Phase 1: Runner Infrastructure

Build the core runner module that all example files will use.

**Files**:
- `examples/__init__.py` — empty package marker
- `examples/_runner.py` — ExampleRunner class, ExampleEntry dataclass, fixture save logic

**Runner responsibilities**:
1. Lazy ABConnectAPI initialization (avoid auth cost when listing entries)
2. Entry registration via `add(name, call, response_model=, request_model=, fixture_file=)`
3. CLI argument parsing: `python -m examples.address [entry_name ...]`
4. Per-entry execution: call → validate response is model → serialize → save fixture
5. Error handling: report exceptions per entry without aborting remaining entries
6. List mode: `python -m examples.address --list` to show all entries with metadata

**Fixture save logic**:
- If result is a Pydantic BaseModel: `model.model_dump(by_alias=True, mode="json")`
- If result is a list of models: dump each item
- If result is None (204): skip save, report
- If result is bytes: skip save (binary fixtures not in scope)
- Write to `tests/fixtures/{fixture_file}` as indented JSON

**Exit criteria**: Runner module importable, `python -m examples._runner --help` works.

### Phase 2: Create Missing Example Files

Create the 3 example files that don't exist yet, using the runner pattern from Phase 1.

**Files**:
- `examples/address.py` — AddressEndpoint (2 methods: validate, get_property_type)
- `examples/lookup.py` — LookupEndpoint (4 methods: get_contact_types, get_countries, get_job_statuses, get_items)
- `examples/users.py` — UsersEndpoint (4 methods: list, get_roles, create, update)

**Per file**:
1. Read the endpoint module to enumerate all public methods
2. Read FIXTURES.md to determine which have captured fixtures vs needs-request-data
3. For captured fixtures: populate request parameters with known working values
4. For pending fixtures: add `# TODO: capture fixture — <reason from FIXTURES.md>`
5. Declare response_model, request_model, and fixture_file per entry

**Exit criteria**: 3 new files, each with all public methods represented. `python -m examples.address --list` shows all entries.

### Phase 3: Migrate Existing Simple Examples

Migrate the 11 simpler example files to the runner pattern (files with straightforward 1:1 method coverage).

**Files** (in order):
1. `examples/autoprice.py` (2 methods)
2. `examples/catalog.py` (catalog methods)
3. `examples/sellers.py` (seller methods)
4. `examples/web2lead.py` (web2lead methods)
5. `examples/contacts.py` (contact methods)
6. `examples/companies.py` (8 methods)
7. `examples/documents.py` (document methods)
8. `examples/payments.py` (payment methods)
9. `examples/notes.py` (note methods)
10. `examples/tracking.py` (tracking methods)
11. `examples/timeline.py` (timeline methods)

**Per file**:
1. Read existing example to extract current method calls and parameters
2. Read endpoint module to identify any public methods not in the example
3. Cross-reference FIXTURES.md for fixture status
4. Rewrite as runner-wrapped entries preserving all existing calls
5. Add missing methods as new entries with TODO annotations
6. Annotate pending-fixture entries with TODO comments

**Exit criteria**: All 11 files migrated. No existing method calls lost. Missing methods added.

### Phase 4: Migrate and Expand Complex Examples

Handle the 5 files that need significant expansion or restructuring.

**Files**:
1. `examples/jobs.py` — Expand from 2 to 28+ methods (ACPortal job CRUD, search, pricing, status, update page config, calendar items)
2. `examples/lots.py` — Expand from 1 to all lot methods (list, get, overrides)
3. `examples/shipments.py` — Already has 14 methods but verify completeness, add runner wrapper
4. `examples/forms.py` — Already has methods but verify all 15 form methods are represented
5. `examples/parcels.py` — Verify completeness against endpoint, add runner wrapper

**Per file**:
1. Read endpoint module, enumerate all public methods with Route metadata
2. Read existing example, map current calls to methods
3. For each missing method: create entry with TODO-annotated parameters
4. Cross-reference FIXTURES.md for all method fixture statuses
5. Rewrite in runner pattern

**Exit criteria**: All 5 files complete with full method coverage. `jobs.py` shows all 28+ methods.

### Phase 5: Validation and Cleanup

Verify the migration is complete and consistent.

**Checks**:
1. Every endpoint module in `ab/api/endpoints/` has a corresponding `examples/*.py`
2. Every public method in each endpoint class has a `runner.add()` entry
3. Every entry with a captured fixture (per FIXTURES.md) has populated request parameters
4. Every entry for a pending fixture has a `# TODO` comment
5. `python -m examples.<module> --list` works for all modules
6. Existing test suite passes (no fixture loading breakage)
7. Ruff lint passes on all new/modified files

**Exit criteria**: All checks pass. Ready for commit.

## Complexity Tracking

No constitution violations — table not needed.
