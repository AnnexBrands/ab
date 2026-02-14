# Feature Specification: Progress Report

**Feature Branch**: `003-progress-report`
**Created**: 2026-02-14
**Status**: Draft
**Input**: User description: "Create progress.html to report on items from surface area that require input. If a test errors or is skipped because new constants are required, give step-by-step instructions for the reviewer."

## Clarifications

### Session 2026-02-14

- Q: Should Action Required cover only scaffolded endpoints with pending fixtures (~27), or all unimplemented endpoints (~269)? → A: All unimplemented endpoints — the report covers every endpoint from the surface area, including those with no models or code yet.
- Q: Should test skip/error status come from running pytest, or be inferred from fixture file presence and constants? → A: File-based inference — derive status from fixture file presence on disk and constants file contents, no pytest execution needed.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Implementation Progress at a Glance (Priority: P1)

A reviewer opens `progress.html` in a browser and immediately sees a summary of overall SDK coverage — how many endpoints are done, pending, and not started — broken down by API surface (ACPortal, Catalog, ABC). Color-coded status indicators make it easy to spot what needs attention.

**Why this priority**: The primary value of the report is answering "where are we?" without reading markdown tables or running tests.

**Independent Test**: Can be fully tested by opening the generated HTML file in any browser and verifying the summary counts match `specs/api-surface.md` data.

**Acceptance Scenarios**:

1. **Given** the progress report has been generated, **When** a reviewer opens `progress.html`, **Then** they see a summary table with total/done/pending/not-started counts per API surface.
2. **Given** the report is open, **When** the reviewer looks at the summary, **Then** each status category uses distinct visual styling (color or icon) so the reviewer can immediately distinguish done from pending from not-started.

---

### User Story 2 - Identify Items Requiring Reviewer Input (Priority: P1)

A reviewer scrolls past the summary to an "Action Required" section listing every unimplemented endpoint from the surface area inventory. Items are organized into tiers by readiness: (1) endpoints with models/code that just need fixture capture or constants, (2) endpoints with no implementation yet that need models, endpoint code, and fixtures. Each item includes its current status and what is needed next.

**Why this priority**: Equally critical to the summary — this is the core purpose. The reviewer must see the full picture of remaining work, not just the subset that is closest to done.

**Independent Test**: Can be tested by verifying every endpoint from `specs/api-surface.md` that is not marked "done" appears in the action-required section.

**Acceptance Scenarios**:

1. **Given** `specs/api-surface.md` lists endpoints with status `pending` or `—`, **When** the report is generated, **Then** all unimplemented endpoints appear in the "Action Required" section with their endpoint path, method, response model, and current status.
2. **Given** a pending endpoint has models and code but no fixture, **When** the reviewer views that item, **Then** it shows fixture capture instructions (SDK method, target file path, blocker reason).
3. **Given** a not-started endpoint has no models or code yet, **When** the reviewer views that item, **Then** it shows the endpoint needs implementation first, along with the endpoint group and ABConnectTools reference status.
4. **Given** an item requires a new constant (e.g., a specific job ID with shipment data), **When** the reviewer views that item, **Then** the report shows which constant is needed and where to add it.

---

### User Story 3 - Follow Step-by-Step Instructions to Resolve a Blocked Item (Priority: P1)

For each action-required item, the report provides step-by-step instructions the reviewer can follow to unblock it. Instructions cover: how to call the endpoint (SDK method or curl), what staging entity to use, where to save the captured fixture, and how to update `tests/constants.py` if a new constant is needed.

**Why this priority**: Without actionable instructions, the reviewer still has to reverse-engineer what to do. The instructions are the payoff of the entire report.

**Independent Test**: Can be tested by following the instructions for one pending fixture and confirming the test passes afterward.

**Acceptance Scenarios**:

1. **Given** a pending fixture for an endpoint like `/job/{id}/timeline`, **When** the reviewer reads its instructions, **Then** the steps include: (a) find a staging entity with the required data, (b) call the SDK method or API endpoint, (c) save the response to the correct fixture file path, (d) re-run the test to confirm it passes.
2. **Given** a fixture that requires a new constant (e.g., a shipped job ID for tracking), **When** the reviewer reads the instructions, **Then** the steps include: (a) identify a valid entity in staging, (b) add the constant to `tests/constants.py` with a descriptive name, (c) capture the fixture using that constant, (d) re-run the affected tests.
3. **Given** a fixture that is blocked by environment limitations (e.g., "no catalog data in staging"), **When** the reviewer reads its instructions, **Then** the report clearly states the blocker cannot be resolved in staging and suggests alternative approaches (production capture, mock approval, or deferral).

---

### User Story 4 - Regenerate the Report After Making Changes (Priority: P2)

After the reviewer captures a fixture or adds a constant, they regenerate the report by running a single command. The updated report reflects the new state — the resolved item moves from "Action Required" to "Done" and the summary counts update.

**Why this priority**: Regeneration closes the feedback loop. Without it, the reviewer can't confirm their work resolved the issue without manually checking.

**Independent Test**: Can be tested by capturing one pending fixture, regenerating the report, and confirming the item's status changed.

**Acceptance Scenarios**:

1. **Given** the reviewer has captured a fixture and saved it to `tests/fixtures/`, **When** they regenerate the report, **Then** that endpoint moves out of "Action Required" and the pending count decreases by one.
2. **Given** no fixtures or constants have changed since the last generation, **When** the reviewer regenerates the report, **Then** the output is identical to the previous version.

---

### Edge Cases

- What happens when `FIXTURES.md` or `specs/api-surface.md` is missing or malformed? The generator should fail with a clear error message identifying which file is missing.
- What happens when a fixture file exists in `tests/fixtures/` but is not listed in `FIXTURES.md`? The report should still count it as captured (filesystem is the source of truth for existence).
- What happens when a new endpoint is added to `api-surface.md` but not yet reflected in `FIXTURES.md`? The report should show it as "not started" (no fixture, no pending entry).
- What happens when `tests/constants.py` already defines a constant that a pending fixture needs? The instructions should note the constant exists and skip the "add constant" step.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST generate a self-contained `progress.html` file that can be opened in any modern browser without a web server or external dependencies.
- **FR-002**: System MUST parse `specs/api-surface.md` to extract all endpoint groups, their implementation status (done/pending/not started), and coverage counts per API surface.
- **FR-003**: System MUST parse `FIXTURES.md` to extract pending fixtures with their blocker reasons and capture instructions.
- **FR-004**: System MUST scan `tests/fixtures/` directory to determine which fixture files actually exist on disk (source of truth for fixture availability).
- **FR-005**: System MUST display a summary section with total/done/pending/not-started counts per API surface (ACPortal, Catalog, ABC) and an overall total.
- **FR-006**: System MUST display an "Action Required" section listing every unimplemented endpoint from the surface area, organized into tiers: (1) scaffolded endpoints needing fixture capture or constants, (2) not-started endpoints needing full implementation. Within each tier, items are grouped by endpoint group.
- **FR-007**: For each action-required item, the system MUST display step-by-step instructions that a reviewer can follow to resolve the blocker.
- **FR-008**: Step-by-step instructions for fixture capture MUST include: the SDK method call, the target fixture file path, and the test command to verify.
- **FR-009**: Step-by-step instructions for new constants MUST include: the constant name to add, the file to edit (`tests/constants.py`), how to find a valid entity in staging, and which tests use the constant.
- **FR-010**: Items blocked by environment limitations (no staging data) MUST be clearly distinguished from items that the reviewer can resolve, with an explanation of why they are blocked.
- **FR-011**: System MUST be runnable via a single command from the repository root.
- **FR-012**: System MUST read `tests/constants.py` to determine which constants already exist, so instructions do not ask the reviewer to add a constant that is already defined.
- **FR-013**: System MUST determine test skip/error status by file-based inference (fixture file presence in `tests/fixtures/` and constant definitions in `tests/constants.py`) — not by executing pytest or parsing test output.

### Key Entities

- **Endpoint**: An API route with method, path, response model, and implementation status (done/pending/not started).
- **Fixture**: A captured JSON API response stored in `tests/fixtures/`. Can be captured (file exists) or pending (file missing, needs human action).
- **Constant**: A test identifier in `tests/constants.py` (e.g., `LIVE_COMPANY_UUID`) needed to call certain endpoints during fixture capture.
- **Blocker**: The reason a pending fixture cannot be captured automatically — environment limitation, missing constant, or entity-state dependency.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The generated report accounts for 100% of endpoints listed in `specs/api-surface.md` — no endpoint is missing from the report.
- **SC-002**: Every unimplemented endpoint from `specs/api-surface.md` appears in the "Action Required" section — pending fixtures with blocker reasons and step-by-step instructions, and not-started endpoints with their implementation status.
- **SC-003**: A reviewer unfamiliar with the codebase can follow the instructions for any resolvable item and successfully capture the fixture or add the constant within 10 minutes per item.
- **SC-004**: After resolving an item and regenerating the report, the item's status updates correctly within one regeneration cycle.
- **SC-005**: The report opens and renders correctly in Chrome, Firefox, and Safari without any external network requests.

## Assumptions

- The report generator runs from the repository root and accesses all project files via relative paths.
- `specs/api-surface.md` follows the current table format with `| AB |` column values of `done`, `pending`, or `—`.
- `FIXTURES.md` follows the current two-table format (Captured Fixtures, Pending Fixtures) with consistent column headers.
- The reviewer has staging API credentials configured (`.env.staging`) to capture fixtures.
- Constants in `tests/constants.py` follow the `LIVE_*` naming convention.
- Test skip/error status is inferred from file presence (a missing fixture file means the corresponding test would skip via `require_fixture`), not from pytest execution.
