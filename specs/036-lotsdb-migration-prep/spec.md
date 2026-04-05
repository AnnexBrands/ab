# Feature Specification: Lotsdb Migration Prep — Replace ABConnectTools with `ab`

**Feature Branch**: `036-lotsdb-migration-prep`
**Created**: 2026-04-04
**Status**: Draft
**Input**: User description: "prepare to replace package /opt/pack/ABConnectTools in site /src/lotsdb. double check each endpoint has and supports fixture details for request params, query, and body. write ab_migrate.md and mention anywhere the ab library is not backward compatible with ABConnectTools. if needed, check swagger or abconnect code as tiebreaker for correct implementation. we want all endpoints to implement actual api."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Lotsdb engineer follows a migration guide to swap `ABConnectTools` for `ab` (Priority: P1)

A Lotsdb engineer needs a single authoritative document (`ab_migrate.md`) that enumerates every place `ABConnectTools` (the `ABConnect` package) behaves differently from the new `ab` SDK, so they can rewrite imports, constructor calls, exception handling, and model references in Lotsdb with confidence.

**Why this priority**: Without this document, Lotsdb engineers have to reverse-engineer the new SDK while rewriting production code — the single largest risk in the migration. Every other deliverable feeds into or depends on this guide.

**Independent Test**: A reviewer reads `ab_migrate.md`, then performs a dry-run migration on the known Lotsdb call sites (e.g. `catalog/services.py`, `catalog/views/auth.py`, `catalog/importers.py`, `catalog/management/commands/import_catalog.py`, `catalog/views/recovery.py`) using only the guide. Every change needed maps cleanly to a guide section — no unexplained breakage.

**Acceptance Scenarios**:

1. **Given** a Lotsdb module that imports `from ABConnect import ABConnectAPI, FileLoader`, **When** the engineer consults `ab_migrate.md`, **Then** they find the exact replacement imports (including any symbols that are no longer exported top-level) and the rationale for the change.
2. **Given** Lotsdb code that catches `LoginFailedError` or `NotLoggedInError`, **When** the engineer consults the guide, **Then** it lists which exceptions were removed, renamed, or restructured, what to catch instead, and how the error payload shape changed (`code`, `details`, `to_dict()`).
3. **Given** Lotsdb code calling `ABConnectAPI(request=request, username=..., password=...)`, **When** the engineer consults the guide, **Then** it documents the new constructor signature and the supported authentication flow for Django-`request`-backed sessions.
4. **Given** Lotsdb code importing `from ABConnect.api.models.catalog import AddLotRequest, LotDataDto, LotCatalogDto, UpdateLotRequest`, **When** the engineer consults the guide, **Then** it lists the new module path for each moved symbol and flags any that are not yet ported.

---

### User Story 2 — Every endpoint in `ab` can be driven by request fixtures covering path params, query, and body (Priority: P1)

Before Lotsdb is cut over, every endpoint method in `ab` must have fixture coverage for each category of input it accepts — path parameters, query string parameters, and request body — so Lotsdb tests (and the `ab` test suite) can exercise the real request shape end-to-end without live credentials.

**Why this priority**: Lotsdb will replace direct HTTP calls with `ab` endpoint methods. If any endpoint is missing fixture coverage for one of its input categories, downstream tests cannot mock it deterministically, and regressions may only surface in production.

**Independent Test**: Run an audit that enumerates every public endpoint method in `ab/api/endpoints/*.py`, inspects its declared path params / query params / body model, and confirms a corresponding fixture exists in `tests/fixtures/requests/` (or documents why a category does not apply, e.g. an endpoint with no body). The audit report lists zero gaps.

**Acceptance Scenarios**:

1. **Given** an endpoint method with path params, query params, and a body model, **When** the fixture audit runs, **Then** a request fixture exists for each category and the audit reports "complete".
2. **Given** an endpoint that only accepts path params (no query, no body), **When** the audit runs, **Then** it records the endpoint as "N/A for query/body" with justification pulled from the route definition, not flagged as missing.
3. **Given** an endpoint whose current implementation is a stub (returns a hardcoded value or `NotImplementedError`), **When** the audit runs, **Then** that endpoint is flagged as "not calling actual API" and blocks the migration-ready state.

---

### User Story 3 — Every endpoint calls the actual upstream API (no stubs) (Priority: P1)

Every endpoint method exposed by `ab` must issue a real HTTP request to the correct upstream route (acportal / catalog / abc), with the correct method, path, param binding, and body serialization. Any stubbed, placeholder, or partially implemented endpoint is a blocker for the Lotsdb cutover.

**Why this priority**: Lotsdb users will hit production data through these endpoints. A stub that silently returns fake data would be a severe defect once Lotsdb is live.

**Independent Test**: Cross-check each endpoint method against (a) the swagger definition for the corresponding route and (b) the `ABConnectTools` implementation. For each endpoint confirm: HTTP verb matches, path template matches, path/query/body binding matches, and response parsing matches. Any discrepancy is logged with swagger/`ABConnectTools` as tiebreaker.

**Acceptance Scenarios**:

1. **Given** an endpoint in `ab`, **When** compared to swagger, **Then** the HTTP verb and URL template are identical.
2. **Given** a conflict between `ab` and `ABConnectTools` behavior, **When** swagger resolves the conflict, **Then** `ab` is corrected to match swagger and the decision is recorded in `ab_migrate.md`.
3. **Given** a conflict where swagger is silent or ambiguous, **When** `ABConnectTools` is used as tiebreaker, **Then** the decision and justification are recorded in `ab_migrate.md`.

---

### User Story 4 — Lotsdb call-site inventory maps old usage to new usage (Priority: P2)

The migration prep produces a checklist of every Lotsdb file, symbol, and line that references `ABConnect`/`ABConnectTools`, with the exact `ab` replacement for each. This becomes the execution checklist for the actual cutover PR in Lotsdb.

**Why this priority**: The document in Story 1 explains the rules; this inventory applies those rules to the known call sites so the cutover PR is mechanical.

**Independent Test**: Every file returned by searching Lotsdb for `ABConnect` references appears in the inventory with an explicit replacement or a "no change needed" note.

**Acceptance Scenarios**:

1. **Given** the inventory, **When** a reviewer greps Lotsdb for `ABConnect`, **Then** every hit is represented in the inventory.
2. **Given** an inventory entry, **When** a reviewer applies the suggested change to the corresponding Lotsdb file, **Then** the file’s intent is preserved and imports/types resolve against `ab`.

---

### Edge Cases

- **Symbol removed, no replacement**: `ABConnectTools` exports (`APIRequestBuilder`, `Quoter`, `FileLoader`, `ABConnect.models`, `ABConnect.routes`) that are not present in `ab`. The guide must state whether the symbol is removed, replaced, or out-of-scope for the migration, and point Lotsdb at an alternative or flag the caller for rewrite.
- **Exception shape change**: Code that relies on `ABConnectError.code`, `.details`, or `.to_dict()` continues to "work" at import time but silently loses information because the new `ABConnectError` does not carry those attributes. The guide must flag every attribute access pattern, not just the class name.
- **Model moved between modules**: Lot-related request/response models moved from `ABConnect.api.models.catalog` to `ab.api.models.lots`. Any import from the old path fails; the guide and inventory must catch this.
- **Constructor signature narrowed**: `ABConnectAPI` no longer accepts positional or keyword `username`/`password`. Any call site that passed credentials must be redirected to the supported authentication path.
- **Endpoint exists in `ABConnectTools` but not in `ab`** (or vice versa): The audit may discover endpoints with no counterpart. The guide must list these with a recommended action (port, skip, block cutover).
- **Fixture exists but does not match current model**: A fixture file may exist under the old shape; the audit must compare against the current request model, not just file presence.
- **Endpoint using path param that is not exposed as a fixture category**: Some endpoints take an ID directly as a function argument rather than a bound param — the audit must still confirm the fixture represents a realistic value.
- **Swagger and `ABConnectTools` disagree**: Swagger wins; the decision is logged.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The migration guide (`ab_migrate.md`, located at the repo root of `ab`) MUST enumerate every public symbol exported by `ABConnectTools` (`ABConnect/__init__.py`, `ABConnect.exceptions`, `ABConnect.api.*`, `ABConnect.models`, `ABConnect.routes`) and state, for each, whether `ab` exports an equivalent, a renamed equivalent, a moved equivalent, or has no equivalent.
- **FR-002**: The migration guide MUST document every backward-incompatible change between `ABConnectTools` and `ab`, including at minimum: package/import name change, exception class removals and attribute shape changes, `ABConnectAPI` constructor signature, model module relocations, and removed helpers (`FileLoader`, `APIRequestBuilder`, `Quoter`, `ABConnect.models`/`routes` aliases).
- **FR-003**: For each incompatibility, the migration guide MUST include a "before" snippet (typical `ABConnectTools` usage) and an "after" snippet (equivalent `ab` usage), plus a one-line rationale when behavior changes (not just a rename).
- **FR-004**: Every endpoint method in `ab/api/endpoints/*.py` MUST be covered by a fixture audit that records, per method: the declared path params, query params, and body model; the presence or intentional absence of a fixture for each category; and whether the method makes a real HTTP call.
- **FR-005**: The audit MUST produce zero "missing fixture" findings before Lotsdb cutover is declared ready. Any gaps MUST be closed by adding fixtures that reflect the current request model shape, sourced from or validated against swagger.
- **FR-006**: Every endpoint method in `ab` MUST make an actual HTTP call to the upstream API via the shared HTTP client; stubs, hardcoded return values, and `NotImplementedError` placeholders MUST be removed or blocked from being marked migration-ready.
- **FR-007**: When `ab` and `ABConnectTools` disagree on verb, path, or parameter binding, the canonical answer MUST be determined by consulting swagger first, and `ABConnectTools` second as tiebreaker; the resolution MUST be recorded in `ab_migrate.md`.
- **FR-008**: The deliverable MUST include a Lotsdb call-site inventory listing every file in `/src/lotsdb` that references `ABConnect` (imports, symbol use, string references) with the exact replacement or "no change" annotation.
- **FR-009**: The inventory MUST cover at least the files currently known to reference `ABConnect`: `catalog/services.py`, `catalog/importers.py`, `catalog/management/commands/import_catalog.py`, `catalog/views/auth.py`, `catalog/views/sellers.py`, `catalog/views/panels.py`, `catalog/views/recovery.py` — plus any additional files surfaced by a fresh search at execution time.
- **FR-010**: The migration guide MUST explicitly call out exception-handling migrations that are "silently wrong" (import still resolves, but attribute access degrades), such as `except ABConnectError as e: log(e.details)`.
- **FR-011**: The migration guide MUST document the supported authentication modes for `ab.ABConnectAPI`, replacing any prior `username`/`password` kwarg flow used in Lotsdb.
- **FR-012**: The migration guide MUST state the minimum `ab` version Lotsdb should pin to, and the replacement dependency declaration for `pyproject.toml`.
- **FR-013**: The fixture audit output MUST be reproducible: a reviewer re-running it on the same commit MUST get the same pass/fail set.
- **FR-014**: The migration guide MUST call out any endpoint surface that exists in `ABConnectTools` but is not yet available in `ab`, so Lotsdb maintainers can decide whether to block cutover, keep a transitional shim, or drop the caller.

### Key Entities

- **Migration guide (`ab_migrate.md`)**: A human-readable Markdown document at the root of the `ab` repository describing every incompatibility with `ABConnectTools` plus before/after usage.
- **Fixture audit report**: A per-endpoint record of path param / query / body fixture coverage and real-API status.
- **Lotsdb call-site inventory**: A mapping from each `ABConnect`-referencing line in `/src/lotsdb` to its `ab` replacement.
- **Endpoint method**: A public method on a class in `ab/api/endpoints/*.py` that maps to exactly one upstream HTTP route.
- **Request fixture**: A JSON file under `tests/fixtures/requests/` (params, query, or body) whose shape matches the current request model.
- **Tiebreaker sources**: Swagger definitions for the acportal / catalog / abc APIs (authoritative), followed by `ABConnectTools` source (fallback).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A Lotsdb engineer can complete a dry-run migration of all known `ABConnect` call sites using only `ab_migrate.md` and the inventory, without reading the `ab` source.
- **SC-002**: 100% of endpoint methods in `ab` have fixture coverage for every input category they actually accept (path params, query, body), with zero "missing" entries in the audit report.
- **SC-003**: 100% of endpoint methods in `ab` issue a real HTTP request to the upstream API; zero stubs, zero hardcoded responses, zero `NotImplementedError` placeholders remain in the public endpoint surface.
- **SC-004**: Every public symbol exported by `ABConnectTools` is accounted for in `ab_migrate.md` (equivalent, renamed, moved, removed, or out-of-scope). Count of unaccounted-for symbols is zero.
- **SC-005**: Every `ABConnect`-referencing line in `/src/lotsdb` is represented in the call-site inventory. Count of orphan references is zero.
- **SC-006**: For every discrepancy between `ab` and `ABConnectTools`, the migration guide records which source (swagger or `ABConnectTools`) was used as tiebreaker and the decision made. Count of undocumented discrepancies is zero.
- **SC-007**: After the cutover PR is prepared in Lotsdb using these deliverables, the Lotsdb test suite passes without changes to test expectations that are unrelated to the rename.

## Assumptions

- `ab_migrate.md` lives at the root of the `ab` repository (alongside `README.md`), mirroring the precedent set by `FIXTURES.md`.
- `/src/lotsdb` on the current host is the canonical copy of the consuming site; the inventory is generated from a fresh grep at execution time (not copied from this spec).
- Swagger definitions for all three upstream surfaces (acportal, catalog, abc) are available to the implementer. If any surface is missing a swagger definition, `ABConnectTools` source is used as the sole tiebreaker and the gap is recorded.
- The `ab` package name is `ab` (not `ABConnect`); all import replacements in the guide and inventory assume this rename is final.
- Fixture categories map to folders already established in `ab`: request bodies and query/param fixtures under `tests/fixtures/requests/`, response fixtures at the top level of `tests/fixtures/`.
- This feature is preparation only: the actual commit that changes files inside `/src/lotsdb` is a separate PR in the Lotsdb repo, not part of this feature’s deliverables.
- "Migration-ready" means: guide written, audit clean, inventory complete. Shipping the actual Lotsdb PR is out of scope.

## Out of Scope

- Modifying files inside `/src/lotsdb`. This feature only produces documentation and audits inside the `ab` repo.
- Deprecating or deleting the `ABConnectTools` package itself.
- Adding new endpoints to `ab` beyond what is needed to close "stub" or "missing fixture" findings surfaced by the audit.
- Lotsdb-side test infrastructure changes beyond documenting which `ab` test helpers are available.
