# Feature Specification: Verify Artifact Integrity

**Feature Branch**: `006-verify-artifact-integrity`
**Created**: 2026-02-14
**Status**: Draft
**Input**: Verify progress, fixtures, and api-surface all meet specs. Run all examples and raise issues / reverse claim of progress if warnings print or we get anything other than fully passing outputs.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run All Examples and Audit Outputs (Priority: P1)

A developer runs every example in `examples/` against staging and
compares actual results against what the tracking artifacts claim.
Any example that errors, warns, or produces unexpected output is
flagged. Any endpoint claimed as "captured" in FIXTURES.md that
does not actually have a valid fixture file on disk is reversed
to "needs-request-data". Any endpoint claimed as "done" in
api-surface.md whose example fails is downgraded.

**Why this priority**: The tracking documents (FIXTURES.md,
api-surface.md, progress report) are only trustworthy if their
claims match reality. Without verification, false positives
accumulate and erode confidence in the SDK's completeness.

**Independent Test**: Run `python -m examples --list` to see all
entries, then run each module's examples and compare output
against FIXTURES.md claims. Any discrepancy is a finding.

**Acceptance Scenarios**:

1. **Given** an endpoint marked "captured" in FIXTURES.md, **When**
   its example is run against staging, **Then** the example
   succeeds without HTTP errors and the fixture file exists on
   disk in `tests/fixtures/`.
2. **Given** an endpoint marked "captured" but whose example
   errors or whose fixture file is missing, **When** the audit
   runs, **Then** its status is reversed to "needs-request-data"
   with a description of the failure.
3. **Given** an endpoint marked "done" in api-surface.md, **When**
   its example does not exist or errors, **Then** its status is
   downgraded and the discrepancy is logged.

---

### User Story 2 - Cross-Reference Artifact Consistency (Priority: P2)

A developer verifies that FIXTURES.md, api-surface.md, the
`examples/` directory, `tests/fixtures/` directory, and the
progress report all agree with each other. Every endpoint
appears in the right state in all tracking locations.

**Why this priority**: Artifacts can drift apart — an endpoint
could be marked "done" in api-surface.md but missing from
FIXTURES.md, or a fixture file could exist on disk but not be
tracked. Cross-referencing catches these gaps.

**Independent Test**: Parse all tracking artifacts and compare
their endpoint sets. Report any endpoint that appears in one
artifact but not another, or that has contradictory status.

**Acceptance Scenarios**:

1. **Given** a fixture file exists in `tests/fixtures/`, **When**
   the cross-reference runs, **Then** that endpoint MUST appear
   as "captured" in FIXTURES.md.
2. **Given** an endpoint is marked "done" in api-surface.md,
   **When** the cross-reference runs, **Then** a corresponding
   `runner.add()` entry MUST exist in `examples/`.
3. **Given** an endpoint has a `runner.add()` entry with a
   `fixture_file` param, **When** the cross-reference runs,
   **Then** the named fixture file MUST exist on disk.

---

### User Story 3 - Fix and Update Tracking Documents (Priority: P3)

After the audit identifies discrepancies, the tracking documents
are corrected. FIXTURES.md counts are updated, api-surface.md
statuses are corrected, and the progress report regenerated to
reflect verified reality.

**Why this priority**: The audit findings from US1 and US2 are
only valuable if they result in corrected documents. This story
closes the loop.

**Independent Test**: After corrections, re-run the audit from
US1/US2 and confirm zero discrepancies.

**Acceptance Scenarios**:

1. **Given** the audit found N discrepancies, **When** corrections
   are applied, **Then** re-running the audit produces zero
   findings.
2. **Given** FIXTURES.md captured count was X, **When** some
   endpoints are reversed, **Then** the new count equals the
   number of fixture files actually on disk with valid content.
3. **Given** api-surface.md claimed Y endpoints "done", **When**
   corrections are applied, **Then** only endpoints with passing
   examples retain "done" status.

---

### Edge Cases

- What happens when an example succeeds but returns an empty
  or null response (200 with no data)?
- What happens when a fixture file exists but is malformed or
  cannot be parsed by the Pydantic model?
- What happens when an endpoint exists in the SDK code but has
  no example at all?
- What happens when staging credentials are expired or the
  staging server is down during the audit?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The audit MUST run every `runner.add()` entry in
  `examples/` against the staging environment and record whether
  it succeeds (200), errors (HTTP error), or warns (unexpected
  output).
- **FR-002**: For every endpoint marked "captured" in FIXTURES.md,
  the audit MUST verify the corresponding fixture file exists in
  `tests/fixtures/` and is valid (non-empty, parseable).
- **FR-003**: For every endpoint marked "done" in api-surface.md,
  the audit MUST verify a corresponding example entry exists and
  that the endpoint's method exists in the SDK.
- **FR-004**: Any endpoint that fails verification MUST have its
  status reversed in the tracking document (captured → needs-
  request-data, done → pending) with a note explaining why.
- **FR-005**: The audit MUST produce a summary report listing
  total endpoints checked, passed, failed, and reversed.
- **FR-006**: After corrections, the FIXTURES.md summary counts
  MUST match the actual number of entries in each status section.
- **FR-007**: The progress report MUST be regenerated after
  corrections to reflect verified state.

### Key Entities

- **Endpoint Claim**: An assertion in a tracking document that an
  endpoint has a certain status (captured, done, needs-request-data).
  Key attributes: endpoint path, HTTP method, claimed status,
  source document.
- **Audit Finding**: A discrepancy between a claim and reality.
  Key attributes: endpoint path, claimed status, actual status,
  failure reason, source document.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of endpoints marked "captured" in FIXTURES.md
  have a corresponding fixture file on disk that parses without
  error.
- **SC-002**: 100% of endpoints marked "done" in api-surface.md
  have a corresponding example entry and SDK method.
- **SC-003**: Zero discrepancies between FIXTURES.md, api-surface.md,
  and the examples directory after corrections are applied.
- **SC-004**: The FIXTURES.md captured count matches the actual
  number of fixture files on disk.
- **SC-005**: All examples that are expected to succeed run
  without HTTP errors or unexpected warnings against staging.

### Assumptions

- Staging environment is accessible and credentials are valid
  during the audit run.
- The audit does not create new fixtures — it only verifies
  existing claims. New fixture capture is a separate activity.
- Endpoints marked "needs-request-data" are expected to fail
  and are not counted as discrepancies.
- The audit scope is limited to endpoints currently tracked in
  FIXTURES.md and api-surface.md — unimplemented endpoints are
  out of scope.
