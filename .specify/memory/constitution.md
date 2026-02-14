<!--
  Sync Impact Report
  ==================
  Version change: 1.2.0 → 2.0.0
  Bump rationale: MAJOR — Principle V redefined (Mock Tracking →
    Pending Fixture Tracking), Principle VIII added (Phase-Based
    Context Recovery), Principle II rewritten (fabricated mocks
    prohibited), Development Workflow replaced with DISCOVER phases.
  Modified principles:
    - II. Fixture-Driven Development: Rewritten. Fabricated mocks
      prohibited. Fixtures MUST come from real API responses or
      validated legacy data. Missing fixtures cause test skips with
      capture instructions, not fake data.
    - V. Mock Tracking & Transparency → V. Pending Fixture Tracking:
      Renamed and redefined. MOCKS.md replaced by FIXTURES.md as a
      capture-status tracker. No more fabricated data registry.
  Added principles:
    - VIII. Phase-Based Context Recovery: Work organized into
      discrete phases with checkpoint artifacts. Enables clean
      resume after context loss.
  Added sections:
    - Development Workflow: Replaced with DISCOVER phase model
      referencing .claude/workflows/DISCOVER.md.
  Removed sections: None (old Development Workflow replaced)
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ no update needed
    - .specify/templates/spec-template.md ✅ no update needed
    - .specify/templates/tasks-template.md ✅ no update needed
      (phase names are generic; DISCOVER is a runtime workflow)
  Follow-up TODOs:
    - Create .claude/workflows/DISCOVER.md with mermaid diagram
    - Delete fabricated mock fixtures from tests/fixtures/
    - Rename MOCKS.md → FIXTURES.md and convert to new format
    - Update test files: replace @pytest.mark.mock on fabricated
      fixtures with pytest.skip() + capture instructions
    - Remove capture_fixtures*.py scripts (ad-hoc, replace with
      documented capture procedure in DISCOVER.md)
-->
# ABConnect SDK Constitution

## Core Principles

### I. Pydantic Model Fidelity

Every API response and request body MUST resolve to a validated
Pydantic model. Models MUST use mixin-based inheritance
(IdentifiedModel, TimestampedModel, ActiveModel, CompanyRelatedModel,
JobRelatedModel, FullAuditModel, CompanyAuditModel, JobAuditModel)
so that common fields are defined once and composed explicitly.

- All models MUST inherit from `ABConnectBaseModel`.
  Request models MUST use `extra="forbid"` (via `RequestModel`)
  to catch typos and invalid outbound fields. Response models
  MUST use `extra="allow"` (via `ResponseModel`) so that API
  field additions do not break deserialization. Extra fields
  MUST be logged via `logger.warning` in `model_post_init` to
  surface drift immediately. Fixture validation tests catch
  new response fields on next capture via snapshot comparison.
- Field names MUST be snake_case with camelCase aliases matching
  the actual API JSON keys.
- All fields MUST declare explicit `Optional[...]` when nullable.
- Models MUST include Field descriptions for Sphinx autodoc.
- When swagger declares a schema that contradicts real API
  responses, the model MUST match reality and include a comment
  documenting the swagger deviation.

### II. Fixture-Driven Development

Every endpoint MUST have at least one fixture — a real JSON
response stored in `tests/fixtures/`. Fixtures MUST come from
one of two sources:

1. **Human-captured** — saved by a developer from an actual API
   call to staging or production.
2. **Legacy-validated** — extracted from the legacy ABConnectTools
   project (`/usr/src/pkgs/ABConnectTools/`) where the fixture has
   been confirmed to match real API responses.

Fabricated fixtures (invented JSON that has never been validated
against a real API response) are **prohibited**.

- Fixtures are the source of truth for model correctness.
- New endpoints MUST NOT be considered complete until a real
  fixture is captured and validates against the Pydantic model.
- When a fixture is not yet available, the model test MUST exist
  but MUST use `pytest.skip()` with an actionable message:
  ```python
  pytest.skip(
      "Fixture needed: capture {ModelName}.json via "
      "{HTTP_METHOD} {endpoint_path}"
  )
  ```
- Fixture files MUST be named `{ModelName}.json` and placed in
  `tests/fixtures/`.
- `FIXTURES.md` at the repository root MUST track every
  endpoint's fixture status. See Principle V.

### III. Four-Way Harmony (NON-NEGOTIABLE)

For every API endpoint, four artifacts MUST exist and remain
mutually consistent:

1. **Implementation** (`ab/api/endpoints/` + `ab/api/models/`)
   — endpoint class method and Pydantic model.
2. **Fixture & Test** (`tests/`) — captured fixture validating
   against the model; test covering both fixture validation and
   live call (when safe).
3. **Example** (`examples/`) — runnable Python demonstrating
   endpoint usage and expected output shape.
4. **Sphinx Documentation** (`docs/`) — RST/MyST page with
   endpoint description, example code block, link to the model
   class, and link to the example file.

Adding or modifying any one artifact MUST trigger review of the
other three. An endpoint missing any artifact is incomplete.

Endpoints awaiting fixture capture (Principle II) are tracked as
**partial** — they have implementation + skeleton test but lack
a captured fixture. Partial endpoints MUST NOT be merged to main
without at least a skip-marked test.

### IV. Swagger-Informed, Reality-Validated

The three swagger specs (ACPortal, Catalog-API, ABC-API) are
reference inputs, not authoritative contracts. ACPortal swagger
in particular is known to frequently omit fields, declare wrong
types, or miss entire response models.

- Route definitions MUST reference swagger operation IDs where
  available.
- Models MUST be validated against real API responses (fixtures),
  not solely against swagger schemas.
- Swagger compliance tests MUST alert when new endpoints appear
  in swagger that are not yet implemented, but model correctness
  is determined by fixture validation.
- When a model intentionally deviates from swagger, the deviation
  MUST be documented with a comment on the affected field(s).

### V. Pending Fixture Tracking

Every endpoint's fixture status MUST be tracked in `FIXTURES.md`
at the repository root. Each entry MUST include:

- Endpoint path and HTTP method.
- Model name.
- Status: **captured** (real fixture exists) or **pending**
  (needs human capture).
- For **captured**: date captured and source (staging, production,
  or legacy-validated).
- For **pending**: capture instructions — the exact API call,
  required parameters, prerequisites, and any known blockers
  (e.g., "requires admin role", "needs active shipment on job").

Rules:

- Tests for endpoints with `pending` fixtures MUST skip with
  an actionable message, NOT fabricate data.
- `FIXTURES.md` MUST be updated whenever a fixture is captured
  or a new endpoint is added.
- The pending fixture count MUST be visible in test output
  (pytest skip summary).
- When a fixture is captured, the test MUST be updated to remove
  the skip and add `@pytest.mark.live`.

### VI. Documentation Completeness

Every public endpoint method, request model, and response model
MUST have Sphinx documentation that includes:

- A one-line summary and detailed description.
- The HTTP method and path.
- An inline code example showing Python usage.
- A cross-reference link (`.. autoclass::` or `:class:`) to the
  Pydantic model.
- Parameter descriptions with types.

Documentation MUST be buildable with `make html` without warnings.
Broken cross-references are build failures.

### VII. Flywheel Evolution

Development priorities, patterns, and engineering themes MUST
evolve through an iterative flywheel rather than top-down decree.
The flywheel stages are:

1. **Stakeholder Input** — Corporate stakeholders surface business
   needs, pain points, and integration priorities. These inputs
   MUST be captured as feature requests or spec amendments.
2. **Showcases** — Working demos, mock integrations, and prototype
   endpoints MUST be presented in regular showcases. Showcases are
   the primary venue for validating that engineering work aligns
   with stakeholder expectations.
3. **Guidelines** — Patterns that succeed in showcases MUST be
   distilled into reusable guidelines (coding patterns, model
   conventions, endpoint design idioms). Winning demos propagate:
   a pattern proven in a showcase MUST be promoted to a guideline
   rather than remaining ad-hoc.
4. **Agents.md** — Proven guidelines MUST be encoded into the
   project's `CLAUDE.md` (agent guidance file) so that all future
   development — human or AI-assisted — follows the validated
   patterns automatically.
5. **Engineering Themes** — Recurring guidelines and stakeholder
   priorities MUST be synthesized into engineering themes (e.g.,
   "bulk operations quarter", "catalog reliability sprint") that
   inform the next cycle of spec prioritization.

The flywheel is continuous: engineering themes feed back into
stakeholder discussions, closing the loop. Each full rotation
MUST produce at least one measurable improvement to guidelines
or agent guidance.

- Showcases that receive positive stakeholder validation MUST
  be tagged for propagation into permanent fixtures, examples,
  or guidelines within the same sprint.
- Engineering themes MUST be reviewed and updated at least once
  per planning cycle.
- The `CLAUDE.md` agent guidance file MUST NOT be treated as
  static; it is a living artifact that evolves with each flywheel
  rotation.

### VIII. Phase-Based Context Recovery

Development work MUST be organized into discrete phases with
explicit entry conditions, exit criteria, and checkpoint
artifacts. This ensures that work can be resumed by a new agent
context (or human) without loss of progress.

- Each work phase MUST produce a checkpoint artifact (committed
  file, updated tracking document, or passing test) before the
  phase is considered complete.
- Phase transitions MUST be committed to git. Uncommitted work
  spanning multiple phases is prohibited.
- The `.claude/workflows/` directory MUST contain workflow
  definitions with mermaid diagrams documenting phase sequences,
  entry/exit criteria, and recovery procedures.
- When resuming work after context loss, the agent MUST:
  1. Read the relevant workflow definition.
  2. Check `git log` and `git status` to identify the last
     completed phase.
  3. Read `FIXTURES.md` and run `pytest --tb=line` to assess
     current state.
  4. Resume from the next incomplete phase — never restart from
     scratch.
- Work sessions MUST begin with a state assessment and end with
  a checkpoint commit. If a session cannot complete its current
  phase, progress MUST be committed as work-in-progress with
  clear notes on remaining steps.
- Each feature's `specs/{NNN}/tasks.md` MUST use checkbox tasks
  (`- [ ]` / `- [x]`) so that progress is machine-readable
  across context boundaries.

## API Coverage & Scope

This SDK covers three ABConnect API surfaces:

| API | Base URL (staging) | Swagger |
|-----|-------------------|---------|
| ACPortal | `portal.staging.abconnect.co/api/api` | `/swagger/v1/swagger.json` |
| Catalog | `catalog-api.staging.abconnect.co/api` | `/swagger/v1/swagger.json` |
| ABC | `api.staging.abconnect.co/api` | `/swagger/v1/swagger.json` |

- ACPortal is the largest surface (~220+ endpoints) covering
  companies, contacts, jobs, documents, settings, and more.
- Catalog API manages catalogs, lots, and sellers.
- ABC API handles quoting (quick quote, quote request),
  job updates, reporting, and web leads.

All three APIs share the same identity server for authentication
(OAuth2 password + refresh token grants). The SDK MUST provide a
unified client that routes to the correct base URL transparently.

URL format: ACPortal uses double-`/api/api/` prefix; Catalog uses
single `/api/` prefix. The SDK MUST handle this internally.

## Development Workflow

Endpoint development follows the **DISCOVER** phased workflow
defined in `.claude/workflows/DISCOVER.md`. Each phase has
explicit entry/exit criteria to support clean context recovery
(Principle VIII).

### DISCOVER Phases

1. **D — Discover** — Identify unimplemented endpoints from
   swagger specs. Produce a gap analysis with priority groupings.
2. **I — Implement models** — Create Pydantic models from swagger
   schemas and legacy project reference. Write skeleton tests that
   skip with fixture-capture instructions.
3. **S — Scaffold endpoints** — Write endpoint class methods with
   route definitions. Register in `client.py`. Wire models.
4. **C — Capture fixtures** — Human captures real fixtures from
   staging or production. Tests transition from skip to pass.
5. **O — Observe tests** — Run full test suite. Confirm Four-Way
   Harmony artifacts exist. Update `FIXTURES.md`.
6. **V — Verify & commit** — Checkpoint commit. Phase complete
   and recoverable.
7. **E — Examples & docs** — Write runnable examples and Sphinx
   documentation. Final Four-Way Harmony check.
8. **R — Release** — PR ready. All principles satisfied.

### Phase Rules

- Phases D–S (1–3) MAY be executed by an AI agent within a
  single context window.
- Phase C (Capture) MUST involve a human — agents MUST NOT
  fabricate fixture data.
- Each phase MUST produce committed artifacts before proceeding.
- When context is lost mid-phase, resume from the last committed
  checkpoint using Principle VIII recovery procedure.
- Work within phases MAY use batch-by-type strategy (all models
  → all endpoints → all tests across a service group) for
  parallel efficiency.

### Batching Strategy

Work in service groups of 5–15 endpoints:

- Group by API surface (ACPortal, Catalog, ABC).
- Group by domain (jobs/*, companies/*, contacts/*).
- Each batch completes all DISCOVER phases before starting next.
- Prioritize groups by stakeholder need (Principle VII).

## Governance

This constitution is the authoritative source for development
principles in this repository. All code reviews, pull requests,
and implementation decisions MUST be evaluated against these
principles.

- **Amendment procedure**: Any change to this constitution MUST
  be proposed as a PR with a clear rationale. The version MUST
  be incremented per semantic versioning (MAJOR for principle
  removal/redefinition, MINOR for additions, PATCH for
  clarifications).
- **Compliance review**: Every PR MUST include a self-check
  against the Four-Way Harmony principle. Reviewers MUST verify
  that new endpoints satisfy all eight principles.
- **Versioning policy**: This constitution follows MAJOR.MINOR.PATCH
  semantic versioning. The version line below tracks the current
  state.
- **Runtime guidance**: Detailed development commands, environment
  setup, and domain knowledge belong in `CLAUDE.md` or `README.md`,
  not in this constitution. This document governs principles only.
- **Flywheel accountability**: At least one flywheel rotation
  (stakeholder input through engineering themes) MUST complete
  per planning cycle. The outcome MUST be reflected as a
  `CLAUDE.md` update or a constitution amendment.
- **Context recovery**: Every workflow in `.claude/workflows/`
  MUST include a "Resuming Work" section with step-by-step
  instructions for entering mid-flight. Workflows without
  recovery procedures are incomplete.

**Version**: 2.0.0 | **Ratified**: 2026-02-13 | **Last Amended**: 2026-02-14
