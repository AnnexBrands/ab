# Feature Specification: Runnable Example Coverage with Run-and-Verify Progress

**Feature Branch**: `037-example-coverage`
**Created**: 2026-06-05
**Status**: Draft
**Input**: User description: "progress should expect all examples to run and produce a result that matches the fixture. examples with filename beginning with _ are using a deprecated runner. The point of examples is to show a real function call and a real print of the pydantic response. every endpoint should have an example. every example that cannot run and print an expected response should ask the user to paste examples in progress.html where you can capture the save."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Every endpoint has a canonical, real example (Priority: P1)

A developer evaluating or integrating the SDK opens the examples directory (or the
generated docs) and, for any endpoint on any surface (ACPortal, Catalog, ABC),
finds exactly one canonical example that shows a **real** function call
(`api.<group>[.<subgroup>].<method>(...)`) and a **real** printed pydantic
response. The example reads like documentation, not like a test harness — it does
not hide the call behind a runner abstraction.

**Why this priority**: This is the core deliverable and the irreducible unit of
value. Even with no automation around it, a complete set of honest, copy-pasteable
examples is independently useful to every SDK consumer. Everything else
(verification, reporting, capture) exists to keep this set honest.

**Independent Test**: Enumerate every routed endpoint method from live code; assert
each one is demonstrated by exactly one canonical example file that performs a real
call and prints the response. Verifiable without running any example against the
live API.

**Acceptance Scenarios**:

1. **Given** the complete set of routed endpoints derived from live code, **When**
   a developer looks up any one of them, **Then** there is exactly one canonical
   example demonstrating it with a real call and a real printed response.
2. **Given** an example file, **When** a developer reads it, **Then** the function
   call and the printed pydantic response are plainly visible in the source (no
   runner indirection hiding the call).
3. **Given** a newly added endpoint with no example, **When** coverage is checked,
   **Then** the missing example is reported as a gap.

---

### User Story 2 - Progress expects every example to run and match its fixture (Priority: P2)

An SDK maintainer runs the progress report and sees, per endpoint, whether its
example actually runs and whether the response it prints matches the captured
fixture. A read-only example whose output has drifted from its fixture is shown as
failing; an example that has never been captured is shown as awaiting data. The
report cannot silently claim coverage that does not hold, and a check in the
standard (non-live) test run fails if any endpoint lacks a runnable-or-captured
example.

**Why this priority**: Coverage that is never verified rots. Tying every example to
its fixture turns "we have examples" into "our examples are true," which is the
durable guarantee. It depends on US1 existing first.

**Independent Test**: Run the verification harness against the read-only endpoints;
confirm the progress report reflects pass / fail / awaiting-data per endpoint and
that an intentionally drifted fixture turns the corresponding endpoint red. The
non-live coverage check fails when an endpoint has no example.

**Acceptance Scenarios**:

1. **Given** a read-only endpoint with a captured fixture, **When** the harness
   runs its example, **Then** the printed response is compared to the fixture and
   the endpoint is marked passing only on a match.
2. **Given** a read-only endpoint whose fixture no longer matches the live
   response, **When** the harness runs, **Then** that endpoint is marked failing
   and the mismatch is surfaced.
3. **Given** an endpoint with no example at all, **When** the non-live coverage
   check runs, **Then** it fails and names the uncovered endpoint.
4. **Given** the live code changes (route added/removed), **When** the report is
   regenerated, **Then** the run-status view reflects the change with no
   hand-editing (no drift).

---

### User Story 3 - Operator pastes responses for endpoints that cannot be auto-run (Priority: P2)

For endpoints that cannot be exercised automatically — they mutate state
(create/update/delete), require live credentials or identifiers the harness does
not have, or otherwise cannot safely run — the progress report presents an editable
field per endpoint where an operator pastes the real request and/or response. The
operator exports all pastes as a single file and hands it back; the maintainer then
ingests it to produce the captured fixture and the corresponding example. The report
clearly shows which endpoints are still awaiting a paste.

**Why this priority**: Mutating and credential-gated endpoints are a large share of
the surface and can never be auto-run safely. Without a capture path they would be
permanently uncoverable, breaking the US1 guarantee of "every endpoint." This makes
the human-in-the-loop step explicit and low-friction.

**Independent Test**: Mark an endpoint as not-auto-runnable; confirm it appears in
the report with a paste field; paste a sample response, export the capture file,
ingest it, and confirm a fixture and example are produced and the endpoint flips
from awaiting-data to covered.

**Acceptance Scenarios**:

1. **Given** a mutating endpoint, **When** the harness runs, **Then** it is never
   executed automatically and is listed as awaiting paste in the report.
2. **Given** an endpoint awaiting paste, **When** the operator pastes a real
   response and exports the capture file, **Then** the export contains that
   response keyed to the endpoint.
3. **Given** a capture export, **When** the maintainer ingests it, **Then** a
   fixture is written and an example is created/updated for each pasted endpoint,
   and those endpoints are no longer shown as awaiting paste.
4. **Given** the report, **When** an operator views it, **Then** the set of
   endpoints still awaiting a paste is unambiguous.

---

### User Story 4 - Deprecated-runner examples are migrated to plain scripts (Priority: P3)

A maintainer can see which example files still use the deprecated runner (those
whose filename begins with an underscore) and migrate each to the plain-script form
so that the canonical example for every endpoint reads like documentation. When no
endpoint's canonical example depends on the deprecated runner any longer, the
migration is complete.

**Why this priority**: The deprecated runner hides drift between swagger, models,
examples, fixtures, and tests — the exact drift US2 exists to catch. Migration is
necessary for the examples to be honest, but it is mechanical follow-through on US1
rather than new capability, so it trails the first three stories.

**Independent Test**: List example files beginning with an underscore and the
endpoints they back; confirm each such endpoint also has a plain-script canonical
example; confirm the migration tracker reflects remaining work.

**Acceptance Scenarios**:

1. **Given** the set of underscore-prefixed example files, **When** migration
   status is checked, **Then** the report lists which remain and which are done.
2. **Given** a migrated endpoint, **When** a developer reads its canonical example,
   **Then** it uses the plain-script form with a visible call and printed response.
3. **Given** the no-file-deletion policy, **When** a file is migrated, **Then** a
   new plain-script file is produced and any removal of the old file is surfaced as
   an explicit decision rather than done silently.

---

### User Story 5 - Interactive harmony + capture + sign-off app (Priority: P2)

A maintainer opens an interactive app that lists every endpoint with a **left nav**
to drill in by **tag** (swagger) or **path**. For each endpoint they see its
**Four-Way Harmony** (implementation, example, fixture+test with real coverage, and
Sphinx docs), can **log the real HTTP request/response** (persisted), and can
**interactively sign off** that the example, the tests, and the Sphinx docs are
acceptable. Sign-offs and captures persist across sessions.

**Why this priority**: The static report answers "what exists"; this app is where a
human *reviews and accepts* each endpoint and where real example I/O is captured and
retained — turning coverage into audited, signed-off coverage. It is the working
surface for the capture loop (US3) and the harmony check (Constitution III).

**Independent Test**: Launch the app; drill into an endpoint by tag and by path;
toggle the three sign-off checkboxes and confirm they persist after reload; log a
request/response and confirm it is retained; confirm the harmony pillars reflect the
real on-disk/coverage state.

**Acceptance Scenarios**:

1. **Given** the app, **When** a maintainer switches the nav between tag and path
   views, **Then** every endpoint is reachable under both.
2. **Given** an endpoint, **When** the maintainer views it, **Then** its four
   harmony pillars (impl / example / fixture+test / Sphinx) and test coverage are
   shown.
3. **Given** an endpoint, **When** the maintainer checks "example acceptable",
   "tests acceptable", or "Sphinx acceptable", **Then** the choice persists and is
   visible on reload.
4. **Given** an endpoint, **When** the maintainer logs a real HTTP request/response,
   **Then** it is stored and listed for that endpoint.

---

### Edge Cases

- **Binary / no-content responses**: An endpoint that returns bytes (e.g. a
  document download) or no body cannot print a pydantic response or save a JSON
  fixture — it must be classified explicitly (covered-as-binary / awaiting-paste)
  rather than counted as a failing run.
- **List vs. single-model responses**: Examples that return a list of models must
  compare against the fixture element/collection consistently with how the fixture
  was captured.
- **Paginated responses**: An example returning a paginated wrapper must compare in
  a way that is stable across runs (page size / ordering must not cause false
  mismatches).
- **Missing test identifiers/constants**: A read-only endpoint whose example needs
  an identifier that is not configured cannot run — it must be classified as
  awaiting-data, not failing.
- **Non-deterministic fields**: Live responses may contain timestamps or generated
  ids that differ run-to-run; comparison must not flag these as drift if the intent
  is structural fidelity. The spec requires a defined, documented comparison policy
  (see FR-009).
- **Multiple routes sharing a response model**: Several endpoints may map to the
  same fixture model; coverage must be tracked per endpoint, not per fixture file.
- **Malformed paste**: A pasted response that is not valid for the endpoint's model
  must be rejected at ingest with a clear message, not silently written as a
  fixture.
- **Endpoint with no example yet (new route)**: Must surface as an uncovered gap in
  both the report and the non-live coverage check.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST enumerate every routed endpoint method across all
  surfaces (ACPortal, Catalog, ABC) directly from live code, so coverage is
  measured against the real implemented surface and never a hand-maintained list.
- **FR-002**: Each routed endpoint MUST have exactly one canonical example that
  performs a real call to that endpoint and prints the resulting pydantic response.
- **FR-003**: A canonical example MUST make the call and the printed response
  plainly visible in its source and MUST NOT route the call through the deprecated
  runner abstraction.
- **FR-004**: An example that captures a response MUST be able to persist it as the
  endpoint's fixture, so example output and fixture are kept in lock-step.
- **FR-005**: The system MUST provide a way to run examples for read-only endpoints
  and compare each printed/captured response against that endpoint's fixture,
  yielding a per-endpoint status of passing, failing, or awaiting-data.
- **FR-006**: The system MUST NOT automatically execute mutating endpoints
  (create/update/delete); these MUST be classified as awaiting-paste and routed to
  the capture path.
- **FR-007**: The progress report MUST display, per endpoint, its run/verify status
  (passing / failing / awaiting-data) alongside existing coverage information, and
  this view MUST be regenerable from live code with no drift.
- **FR-008**: The standard non-live test run MUST fail if any routed endpoint lacks
  a canonical example (runnable or captured-via-paste), so coverage cannot silently
  regress.
- **FR-009**: The system MUST define and apply a documented comparison policy for
  matching example output to fixtures that distinguishes genuine structural drift
  from expected run-to-run variation (e.g. volatile fields), so passing/failing
  status is meaningful and stable.
- **FR-010**: For any endpoint that cannot be auto-run and printed, the progress
  report MUST present an editable field where an operator can paste the real
  response (and request where applicable), and MUST clearly indicate which
  endpoints are still awaiting a paste.
- **FR-011**: The report MUST let the operator export all pastes as a single
  portable capture artifact without requiring any backend service, so the report
  remains a static, shareable file safe to generate in automation.
- **FR-012**: The system MUST provide a way to ingest a capture artifact and, for
  each pasted endpoint, produce the captured fixture and create or update the
  corresponding canonical example, after which those endpoints are no longer shown
  as awaiting a paste.
- **FR-013**: Ingest MUST validate a pasted response against the endpoint's model
  and reject malformed pastes with a clear message rather than writing an invalid
  fixture.
- **FR-014**: The system MUST report deprecated-runner migration status — which
  underscore-prefixed example files remain and which endpoints they back — and MUST
  treat an endpoint as fully migrated only once its canonical example uses the
  plain-script form.
- **FR-015**: All additions MUST be backward compatible with existing consumers of
  the SDK; no symbol imported by downstream code may be removed or changed in a
  breaking way, and example/report tooling MUST be additive.
- **FR-016**: File migration MUST honor the repository's no-file-deletion policy:
  migrating a file produces a new plain-script file, and any deletion of a source
  file MUST be surfaced as an explicit decision, not performed silently.
- **FR-017**: Endpoints whose responses cannot be represented as a printable
  pydantic/JSON fixture (e.g. binary downloads, empty bodies) MUST be classified
  explicitly so they are neither counted as failing runs nor as uncovered gaps.
- **FR-018**: An interactive app MUST present a left-nav that lets a maintainer drill
  into endpoints by both **path** and **swagger tag**.
- **FR-019**: For each endpoint the app MUST show its **Four-Way Harmony** —
  implementation, example, fixture+test (with real test coverage), and Sphinx docs.
- **FR-020**: The app MUST let a maintainer log the real HTTP request/response for an
  endpoint and persist it (SQLite), retaining example inputs and outputs for review.
- **FR-021**: The app MUST let a maintainer interactively sign off, per endpoint, that
  the **example is acceptable**, the **tests are acceptable**, and the **Sphinx docs
  are acceptable**, and these sign-offs MUST persist across sessions.
- **FR-022**: Sign-off state MUST be exportable to a committed artifact so it survives
  across machines and can feed the report/gates.
- **FR-023**: The interactive app and its persistence MUST add no new runtime
  dependency to the `ab` package (stdlib only); it is dev tooling, separate from the
  static no-drift report.

### Key Entities *(include if feature involves data)*

- **Endpoint**: A single routed method on an endpoint class, identified by its
  dotted accessor (e.g. `api.jobs.payment.list`), HTTP method, and path. The unit
  of coverage.
- **Canonical Example**: The single authoritative demonstration of an endpoint — a
  real call plus a printed response — in plain-script form.
- **Fixture**: The captured response for an endpoint, stored as the source of truth
  the example's output is compared against.
- **Run Status**: The per-endpoint outcome of verification — passing, failing,
  awaiting-data (read-only but uncaptured), awaiting-paste (mutating/credential-
  gated), or covered-as-binary.
- **Capture Artifact**: The single portable file an operator exports from the
  report containing pasted requests/responses keyed by endpoint, consumed by the
  ingest step.
- **Migration Status**: The record of which deprecated-runner (underscore-prefixed)
  example files remain versus have been migrated to plain scripts.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of routed endpoints across all three surfaces have exactly one
  canonical example demonstrating a real call and a real printed response.
- **SC-002**: 100% of read-only endpoints with a captured fixture pass the
  run-and-verify comparison (no unexplained drift between example output and
  fixture).
- **SC-003**: Every endpoint that cannot be auto-run has a paste slot in the
  report, and 100% of pasted endpoints, once their capture is ingested, have both a
  fixture and a canonical example.
- **SC-004**: The progress report shows a run/verify status for every endpoint, and
  regenerating it from unchanged code produces no diff (no-drift), while a route
  added or removed in code is reflected automatically.
- **SC-005**: The non-live coverage check fails on any endpoint missing a canonical
  example, demonstrated by removing one example and observing the failure.
- **SC-006**: Zero endpoints rely on the deprecated runner for their canonical
  example by feature completion; migration status reports zero remaining.
- **SC-007**: No downstream consumer of the SDK breaks — the existing public import
  surface is unchanged and all pre-existing non-live tests continue to pass.

## Assumptions

- The "users" of this feature are SDK developers/maintainers and an operator who
  has access to a live (staging) environment for capturing real responses; it is
  internal developer tooling, not an end-user-facing product.
- "Endpoint" means a routed method (one bound to an HTTP Route). Pure helper methods
  with no Route are out of scope for the one-example-per-endpoint guarantee.
- Read-only means HTTP GET; create/update/delete (POST/PUT/PATCH/DELETE) are treated
  as mutating and never auto-run, consistent with the decided mutation-safety policy.
- Capturing real responses requires valid staging credentials/identifiers, supplied
  out of band by the operator; the automation itself stores no secrets.
- The comparison policy treats structural/field fidelity as the matching criterion;
  a small, documented set of volatile fields may be normalized before comparison.
- Existing infrastructure (the live-code route enumeration, the fixtures directory,
  the progress-report generator, and the standard non-live test run) is the
  foundation this feature extends rather than replaces.

## Dependencies

- Live-code enumeration of routes and endpoint classes (the basis for FR-001).
- The existing fixtures store as the source of truth for comparison (FR-004/FR-005).
- The existing no-drift progress-report generation pipeline (FR-007).
- The standard non-live test run as the home for the coverage gate (FR-008).
- A staging environment and operator access for capturing read-only and pasted
  responses.
