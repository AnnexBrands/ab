<!--
  Sync Impact Report
  ==================
  Version change: 2.0.0 → 2.1.0
  Bump rationale: MINOR — Principle II rewritten (Fixture-Driven
    Development → Example-Driven Fixture Capture), Principle III
    reordered (Example before Fixture), Principle V status taxonomy
    simplified (pending replaced by needs-request-data),
    Development Workflow DISCOVER phases redefined (C = Call &
    Capture via examples, E = Enrich docs). No principles removed
    or incompatibly redefined.
  Modified principles:
    - II. Fixture-Driven Development → II. Example-Driven Fixture
      Capture: Examples are the fixture capture mechanism. Before
      writing an example, research ABConnectTools and swagger for
      required request bodies and params. 200 → save fixture.
      Error → fix the request, not ask for a response fixture.
    - III. Four-Way Harmony: Artifact order changed. Example now
      precedes Fixture & Test (example produces the fixture).
    - V. Pending Fixture Tracking → V. Endpoint Status Tracking:
      Status taxonomy simplified. Generic "pending" replaced by
      "needs-request-data" — every failure is a request problem.
  Added sections: None
  Removed sections: None
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ no update needed
    - .specify/templates/spec-template.md ✅ no update needed
    - .specify/templates/tasks-template.md ✅ no update needed
  Follow-up TODOs: None — all files updated in this revision.
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

### II. Example-Driven Fixture Capture

Every endpoint MUST have a runnable example in `examples/` that
calls the SDK method with correct parameters. Examples are the
primary mechanism for capturing fixtures.

**Before writing an example**, the developer (human or agent) MUST
research the endpoint's requirements from two sources:

1. **ABConnectTools** — Read the legacy endpoint implementation
   (`/usr/src/pkgs/ABConnectTools/ABConnect/api/endpoints/`) and
   examples (`/usr/src/pkgs/ABConnectTools/examples/api/`) to
   understand required parameters, request bodies, and realistic
   test values.
2. **Swagger specs** — Read the swagger schema for parameter
   definitions, required vs optional fields, and request body
   structure.

**The capture loop**:

1. Example calls the endpoint method with researched parameters.
2. **200 response** → save the response body as a fixture in
   `tests/fixtures/{ModelName}.json`. Fixture captured.
3. **Error response** → the EXAMPLE needs fixing, not a response
   fixture. Diagnose what the request is missing:
   - Missing or wrong **query parameters** (e.g., `/address/isvalid`
     needs `street`, `city`, `state`, `zipCode`).
   - Missing or wrong **request body** (e.g.,
     `/AutoPrice/QuoteRequest` needs an items array with weight
     and class fields).
   - Missing **URL parameters** (e.g., `{addressId}` in the path).
   - **Unknown issue** — research ABConnectTools and swagger more
     deeply for edge cases, required headers, or prerequisites.

**Rules**:

- Fabricated fixtures (invented JSON never validated against a real
  API response) are **prohibited**.
- A failed API call MUST NOT be treated as "needs a response
  fixture." It MUST be treated as "example needs correct request
  data." Every failure is a request problem until proven otherwise.
- Fixture files MUST be named `{ModelName}.json` and placed in
  `tests/fixtures/`.
- `FIXTURES.md` at the repository root MUST track every endpoint's
  status. See Principle V.
- When a fixture is not yet available, the model test MUST exist
  but MUST use `pytest.skip()` with an actionable message:
  ```python
  pytest.skip(
      "Fixture needed: run examples/{service}.py — "
      "endpoint needs {what's missing}"
  )
  ```

### III. Four-Way Harmony (NON-NEGOTIABLE)

For every API endpoint, four artifacts MUST exist and remain
mutually consistent:

1. **Implementation** (`ab/api/endpoints/` + `ab/api/models/`)
   — endpoint class method and Pydantic model.
2. **Example** (`examples/`) — runnable Python that calls the
   endpoint with correct parameters. The example is the fixture
   capture instrument (Principle II).
3. **Fixture & Test** (`tests/`) — fixture captured by running
   the example; test validating the fixture against the model.
4. **Sphinx Documentation** (`docs/`) — RST/MyST page with
   endpoint description, example code block, link to the model
   class, and link to the example file.

Adding or modifying any one artifact MUST trigger review of the
other three. An endpoint missing any artifact is incomplete.

Endpoints whose examples do not yet produce a 200 response are
tracked as **partial** in `FIXTURES.md` with a status indicating
what's missing (see Principle V). Partial endpoints MUST NOT be
merged to main without at least a skip-marked test.

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

### V. Endpoint Status Tracking

Every endpoint's status MUST be tracked in `FIXTURES.md` at the
repository root. Each entry MUST include:

- Endpoint path and HTTP method.
- Model name.
- Status: **captured** or **needs-request-data**.
- For **captured**: date captured and source (staging, production,
  or legacy-validated).
- For **needs-request-data**: what the example is missing — the
  specific query parameters, request body fields, or URL parameters
  that must be researched from ABConnectTools or swagger.

Rules:

- Tests for endpoints without captured fixtures MUST skip with
  an actionable message, NOT fabricate data.
- `FIXTURES.md` MUST be updated whenever a fixture is captured,
  an example is written, or a new endpoint is added.
- The non-captured endpoint count MUST be visible in test output
  (pytest skip summary).
- When a fixture is captured, the test MUST be updated to remove
  the skip and add `@pytest.mark.live`.
- Entries MUST NOT use a generic "pending" status. Every
  non-captured endpoint MUST specify what request data is
  missing.

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

1. **D — Determine** — Research the target service group from
   ABConnectTools and swagger. For each endpoint, identify
   required request bodies, URL parameters, query parameters,
   and realistic test values. This research informs Phase E.
2. **I — Implement models** — Create Pydantic models from swagger
   schemas and ABConnectTools patterns. Write skeleton tests that
   skip with actionable messages.
3. **S — Scaffold endpoints** — Write endpoint class methods with
   route definitions. Register in `client.py`. Wire models.
4. **C — Call & Capture** — Write runnable examples using request
   data researched in Phase D. Run examples against staging.
   200 responses become fixtures. Errors are diagnosed as
   request-data problems (Principle II).
5. **O — Observe tests** — Run full test suite. Confirm Four-Way
   Harmony artifacts exist. Update `FIXTURES.md`.
6. **V — Verify & commit** — Checkpoint commit. Phase complete
   and recoverable.
7. **E — Enrich documentation** — Write Sphinx documentation.
   Final Four-Way Harmony check.
8. **R — Release** — PR ready. All principles satisfied.

### Phase Rules

- Phases D–S (1–3) MAY be executed by an AI agent within a
  single context window.
- Phase C (Call & Capture) MUST use request data researched in
  Phase D. Agents MUST NOT fabricate fixture data. If an example
  returns an error, the agent MUST diagnose and fix the request
  (wrong params, missing body fields). Track unresolved endpoints
  as `needs-request-data` in `FIXTURES.md` with specifics.
- Each phase MUST produce committed artifacts before proceeding.
- When context is lost mid-phase, resume from the last committed
  checkpoint using Principle VIII recovery procedure.
- Work within phases MAY use batch-by-type strategy (all models
  → all endpoints → all examples across a service group) for
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

**Version**: 2.1.0 | **Ratified**: 2026-02-13 | **Last Amended**: 2026-02-14
