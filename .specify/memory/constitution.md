<!--
  Sync Impact Report
  ==================
  Version change: 2.2.0 → 2.3.0
  Bump rationale: MINOR — New "Sources of Truth" section added
    between Core Principles and API Coverage & Scope. Codifies a
    three-tier hierarchy: (1) API server source at /src/ABConnect/,
    (2) captured fixtures from real API responses, (3) swagger
    specifications. Driven by stakeholder input: server source has
    always been the ground truth but was never documented in the
    constitution.
  Modified principles:
    - II. Example-Driven Fixture Capture: Added server source as
      research source (step 0, before ABConnectTools and swagger).
      Contextualized fixtures as Tier 2 in the hierarchy.
    - IV. Swagger-Informed, Reality-Validated: Added cross-reference
      to Sources of Truth hierarchy. Clarified swagger's position
      as Tier 3 (informational, not authoritative).
  Added sections:
    - Sources of Truth (new top-level section between Core Principles
      and API Coverage & Scope)
  Removed sections: None
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ no update needed
    - .specify/templates/spec-template.md ✅ no update needed
    - .specify/templates/tasks-template.md ✅ no update needed
  Follow-up TODOs: None
  Propagated changes:
    - .claude/workflows/DISCOVER.md ✅ updated (Phase D server
      source step, server source path reference table)
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
research the endpoint's requirements from these sources, in order
of authority (see Sources of Truth):

0. **API Server Source** (`/src/ABConnect/`) — Read the controller
   action for the endpoint to understand parameter binding, required
   fields, and response construction. Read the DTO classes for exact
   field names and types. This is the definitive source when
   available.
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
     needs `Line1`, `City`, `State`, `Zip` — these are the swagger
     parameter names, not guesses).
   - Missing or wrong **request body** (e.g.,
     `/AutoPrice/QuoteRequest` needs an items array with weight
     and class fields).
   - Wrong **transport** — a POST endpoint sending `params=`
     instead of `json=` will silently drop the request body.
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
   — request json, request params, or response json out of harmony
     with swagger MUST be explicitly excused in `api-surface.md`.
2. **Example** (`examples/`) — runnable Python that calls the
   endpoint with correct parameters. The example is the fixture
   capture instrument (Principle II).
3. **Fixture & Test** (`tests/`) — fixture captured by running
   the example; test validating the fixture against the model.
   - test exists for all endpoints that does not error in HTTP
     or when cast to response model in return
4. **Sphinx Documentation** (`docs/`) — RST/MyST page with
   endpoint description, example code block, repr of model class
   and link to the example file.

Adding or modifying any one artifact MUST trigger review of the
other three. An endpoint missing any artifact is incomplete.

Endpoints whose examples do not yet produce a 200 response are
tracked as **partial** in `FIXTURES.md` with a status indicating
what's missing (see Principle V). Partial endpoints MUST NOT be
merged to main without at least a skip-marked test.

### IV. Swagger-Informed, Reality-Validated

The three swagger specs (ACPortal, Catalog-API, ABC-API) are
reference inputs, not authoritative contracts (Tier 3 in the
Sources of Truth hierarchy). ACPortal swagger in particular is
known to frequently omit fields, declare wrong types, or miss
entire response models. The API server source code is the ultimate
authority (Tier 1); captured fixtures are strong evidence of
actual behavior (Tier 2).

- Route definitions MUST reference swagger operation IDs where
  available.
- Models MUST be validated against real API responses (fixtures),
  not solely against swagger schemas.
- Swagger compliance tests MUST alert when new endpoints appear
  in swagger that are not yet implemented, but model correctness
  is determined by fixture validation.
- When a model intentionally deviates from swagger, the deviation
  MUST be documented with a comment on the affected field(s).
- Query parameter names sent by endpoint methods MUST match
  swagger parameter definitions. `tests/test_example_params.py`
  MUST enforce this automatically by cross-referencing endpoint
  source against swagger specs (Principle IX).

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

### IX. Endpoint Input Validation

Every endpoint method MUST validate its inputs before making
an HTTP call. Unvalidated inputs cause silent failures — the
API ignores unrecognized parameters without returning an error,
producing empty or default responses that appear to work but
carry no user data.

**Request body validation**:

- Endpoints that accept a request body MUST define a Pydantic
  `RequestModel` (with `extra="forbid"`) for that body.
- The endpoint method MUST validate the body against the model
  before sending it. Invalid or extra fields MUST raise a
  `ValidationError` at call time, not silently pass through.
- Required fields in the swagger `requestBody` schema MUST be
  required (not `Optional`) in the Pydantic model.

**Query parameter validation**:

- Parameter names mapped inside endpoint methods MUST match
  the swagger spec's query parameter definitions. Names MUST
  NOT be guessed or invented.
- Python method signatures MUST use snake_case. The mapping to
  the API's PascalCase or camelCase happens inside the method
  body (e.g., `params["Line1"] = line1`).
- Required swagger query parameters SHOULD be required Python
  arguments (not `Optional`) so that callers get a `TypeError`
  at call time rather than a silent 400 or empty response.

**Automated enforcement**:

- `tests/test_example_params.py` MUST cross-reference every
  endpoint method's parameter mappings against the swagger
  specs via static analysis. Unknown parameter names and
  incorrect transport (e.g., `params=` where `json=` is
  required) MUST cause test failure.
- This test MUST run as part of the standard `pytest` suite
  (not gated behind a marker).

**Rationale**: Feature 005 found 5 endpoints where inputs were
silently ignored (`address.validate`, `address.get_property_type`,
`forms.get_operations`, `shipments.request_rate_quotes`,
`documents.list`). In each case, the root cause was that the
endpoint method accepted inputs without validating them against
the swagger contract. Pydantic validation at the SDK boundary
catches these errors before the HTTP call is made.

## Sources of Truth

When information about API behavior conflicts across sources, the
following hierarchy determines which source is authoritative:

1. **API Server Source Code** (`/src/ABConnect/`) — The actual .NET
   server implementation. Controllers define route behavior, DTOs
   define response/request shapes, services implement business logic.
   This is the ultimate authority for what the API does.

   Key paths:
   - ACPortal controllers: `ACPortal/ABC.ACPortal.WebAPI/Controllers/`
   - ACPortal DTOs: `ACPortal/ABC.ACPortal.WebAPI/Models/`
   - ABC controllers: `ABC.WebAPI/Controllers/`
   - ABC DTOs: `ABC.WebAPI/Models/`
   - Shared entities: `AB.ABCEntities/`
   - Business logic: `ABC.Services/`

2. **Captured Fixtures** (`tests/fixtures/`) — Real responses from
   the live API, captured by running examples against staging. These
   are validated evidence of actual API behavior at a point in time.
   Fixtures are strong truth — they reflect what the API actually
   returned.

3. **Swagger Specifications** — Auto-generated OpenAPI specs served
   by each API surface. Useful for endpoint discovery, parameter
   naming, and initial schema research. However, ACPortal swagger
   is known to frequently omit fields, declare wrong types, or miss
   entire response models. Swagger is informational, not
   authoritative.

**Degradation policy**: When a higher-ranked source is unavailable
(e.g., server source not accessible in CI), use the next available
source. When no fixtures exist for a new endpoint, swagger is the
starting reference — track the endpoint as needing validation.

**Conflict resolution**: When sources disagree, the higher-ranked
source wins. If server source contradicts a fixture, re-capture the
fixture. If a fixture contradicts swagger, trust the fixture and
document the swagger deviation.

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
   correct transport type (params vs json), and realistic test
   values. This research informs Phases S and C.
2. **I — Implement models** — Create Pydantic models from swagger
   schemas and ABConnectTools patterns. Write skeleton tests that
   skip with actionable messages.
3. **S — Scaffold endpoints** — Write endpoint class methods with
   route definitions. Register in `client.py`. Wire models.
   Endpoint methods MUST use correct transport (Principle IX)
   and map parameter names to exact swagger names.
4. **C — Call & Capture** — Write runnable examples using request
   data researched in Phase D. Run examples against staging.
   200 responses become fixtures. Errors are diagnosed as
   request-data problems (Principle II).
5. **O — Observe tests** — Run full test suite including
   `tests/test_example_params.py` (Principle IX). Confirm
   Four-Way Harmony artifacts exist. Update `FIXTURES.md`.
6. **V — Verify & commit** — Checkpoint commit. Phase complete
   and recoverable.
7. **E — Enrich documentation** — Write Sphinx documentation.
   Final Four-Way Harmony check.
8. **R — Release** — PR ready. All principles satisfied.

### Phase Rules

- Phases D–S (1–3) MAY be executed by an AI agent within a
  single context window.
- Phase S (Scaffold) MUST verify transport correctness: GET
  endpoints use `params=`, POST/PUT/PATCH with requestBody use
  `json=`. Parameter names MUST match swagger. Run
  `pytest tests/test_example_params.py` as Phase S exit gate.
- Phase C (Call & Capture) MUST use request data researched in
  Phase D. Agents MUST NOT fabricate fixture data. If an example
  returns an error, the agent MUST diagnose and fix the request
  (wrong params, missing body fields, wrong transport). Track
  unresolved endpoints as `needs-request-data` in `FIXTURES.md`
  with specifics.
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
  that new endpoints satisfy all nine principles.
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

**Version**: 2.3.0 | **Ratified**: 2026-02-13 | **Last Amended**: 2026-02-21
