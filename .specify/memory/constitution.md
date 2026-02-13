<!--
  Sync Impact Report
  ==================
  Version change: (none) → 1.0.0
  Modified principles: N/A (initial creation)
  Added sections:
    - Core Principles (6 principles)
    - API Coverage & Scope
    - Development Workflow
    - Governance
  Removed sections: N/A
  Templates requiring updates:
    - .specify/templates/plan-template.md ⚠ pending (no changes needed
      at this time; Constitution Check section is generic)
    - .specify/templates/spec-template.md ⚠ pending (no changes needed
      at this time; template is generic)
    - .specify/templates/tasks-template.md ⚠ pending (no changes needed
      at this time; template is generic)
  Follow-up TODOs: None
-->
# ABConnect SDK Constitution

## Core Principles

### I. Pydantic Model Fidelity

Every API response and request body MUST resolve to a validated
Pydantic model. Models MUST use mixin-based inheritance
(IdentifiedModel, TimestampedModel, ActiveModel, CompanyRelatedModel,
JobRelatedModel, FullAuditModel, CompanyAuditModel, JobAuditModel)
so that common fields are defined once and composed explicitly.

- All models MUST inherit from `ABConnectBaseModel` with
  `extra="forbid"` to catch unexpected fields immediately.
- Field names MUST be snake_case with camelCase aliases matching
  the actual API JSON keys.
- All fields MUST declare explicit `Optional[...]` when nullable.
- Models MUST include Field descriptions for Sphinx autodoc.
- When swagger declares a schema that contradicts real API
  responses, the model MUST match reality and include a comment
  documenting the swagger deviation.

### II. Fixture-Driven Development

Every endpoint MUST have at least one example that returns a
captured fixture (a real JSON response stored in `tests/fixtures/`).
Each fixture MUST validate against its corresponding Pydantic model
without error.

- Fixtures are the source of truth for model correctness.
- New endpoints MUST NOT be considered complete until a fixture
  is captured and validates.
- Where a fixture cannot be obtained from a live API (auth
  restrictions, destructive operations, missing data), a mock
  fixture MUST be created and tracked in `MOCKS.md` at the
  repository root with: endpoint path, reason mock is needed,
  date added, and status (mock / live).
- Fixture files MUST be named `{ModelName}.json` and placed in
  `tests/fixtures/`.

### III. Four-Way Harmony (NON-NEGOTIABLE)

For every API endpoint, four artifacts MUST exist and remain
mutually consistent:

1. **Implementation** (`src/api/endpoints/` + `src/api/models/`)
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

### V. Mock Tracking & Transparency

Any endpoint or fixture that relies on fabricated data rather than
a captured live response MUST be explicitly tracked.

- `MOCKS.md` MUST list every mocked fixture with: endpoint path,
  HTTP method, model name, reason (e.g., "requires admin role",
  "destructive POST"), date added, and resolution status.
- Mocks MUST use realistic data shapes matching known model
  definitions.
- Mocks MUST be replaced with live fixtures as soon as access or
  safe execution becomes available.
- CI/test output SHOULD distinguish mock-validated tests from
  live-validated tests via pytest markers (`@pytest.mark.mock`,
  `@pytest.mark.live`).

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

The mandatory development sequence for each endpoint is:

1. **Document** — Write Sphinx docs and example stub describing
   the endpoint's purpose and expected models.
2. **Model** — Define Pydantic request/response models from
   swagger + any available real responses.
3. **Fixture** — Capture a live response fixture (or create a
   tracked mock if live capture is not possible).
4. **Test** — Write tests that validate the fixture against the
   model and (where safe) make a live API call.
5. **Implement** — Write the endpoint class method with route
   definition, wiring models to request/response validation.
6. **Verify Harmony** — Confirm all four harmony artifacts exist
   and are consistent.

This sequence ensures models are reality-grounded before
implementation code is written.

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
  that new endpoints satisfy all six principles.
- **Versioning policy**: This constitution follows MAJOR.MINOR.PATCH
  semantic versioning. The version line below tracks the current
  state.
- **Runtime guidance**: Detailed development commands, environment
  setup, and domain knowledge belong in `CLAUDE.md` or `README.md`,
  not in this constitution. This document governs principles only.

**Version**: 1.0.0 | **Ratified**: 2026-02-13 | **Last Amended**: 2026-02-13
