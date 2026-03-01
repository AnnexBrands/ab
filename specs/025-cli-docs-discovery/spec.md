# Feature Specification: CLI Docs & Discovery Major Release

**Feature Branch**: `025-cli-docs-discovery`
**Created**: 2026-03-01
**Status**: Draft
**Input**: User description: "do a major release on cli. update sphinx, endpoint docstrings. any call to an endpoint like `ab jobs get --help` should print helpful information like raw uri, python and cli signature/params, return type. make the discovery of constants and fixtures more generic. if `ex jobs get` needs to be explicitly told a model name, question why that is needed. make sure we are tracking progress in an upgraded way. group by path root and tag, show endpoint, method dotted path, ex and cli (ab/abs) for each. enable me to list methods and show help, with progress.html and sphinx giving a nice overview."

## Clarifications

### Session 2026-03-01

- Q: Should CLI output changes be backwards-compatible or a clean redesign? → A: Clean redesign — no backwards compat needed. Additionally, `--list` is never typed explicitly; a parent command with no arguments implicitly lists its children (e.g., `ab` lists groups, `ab jobs` lists methods).
- Q: How should progress tracking group endpoints — by path root or endpoint class? → A: Group by endpoint class (e.g., `jobs`, `contacts`) with sub-sections by path sub-root (e.g., `timeline`, `onhold`). The alias system is shared across CLI (`ab`/`abs`), examples (`ex`), and progress report.
- Q: Should methods without a Route (helpers, composed wrappers) appear in listings? → A: Yes, in a separate "Helpers" section prioritized at the top of the listing, since these are the high-level convenience methods users reach for first.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Rich CLI Help for Any Endpoint (Priority: P1)

A developer runs `ab jobs get_timeline --help` and gets a complete, self-documenting reference card: the raw API URI, the Python SDK call signature, the CLI invocation syntax, all parameters with types and defaults, the return type, and the associated request/response models. This removes the need to open source code or Sphinx docs for quick lookups.

**Why this priority**: This is the single highest-value improvement. Every SDK user hits `--help` dozens of times per day. Currently the output is minimal — it shows parameters but omits the URI, return type, and model names. This is the most frequent friction point.

**Independent Test**: Can be fully tested by running `ab jobs get --help` and verifying the output contains the raw URI (`GET /job/{jobDisplayId}`), Python signature (`api.jobs.get(job_display_id: int) -> Job`), CLI usage (`ab jobs get <job_display_id>`), and return type (`Job`).

**Acceptance Scenarios**:

1. **Given** any endpoint method, **When** the user runs `ab <module> <method> --help`, **Then** the output displays: raw URI, Python signature, CLI syntax, all parameters with types/defaults, and return type.
2. **Given** an endpoint with a request model, **When** `--help` is invoked, **Then** the request model name and its fields are shown.
3. **Given** an endpoint with a params model (query parameters), **When** `--help` is invoked, **Then** the query parameter model and fields are shown.
4. **Given** the `--help` flag, **When** no credentials are configured, **Then** help still displays successfully (no API call needed).

---

### User Story 2 - Route-Derived Model Discovery (Priority: P1)

A developer adding a new example entry with `runner.add("get", lambda api: api.jobs.get(...))` no longer needs to manually specify `response_model="Job"` or `fixture_file="Job.json"`. The system infers these from the Route definition already declared on the endpoint class. Manual model metadata in example entries becomes optional — only needed for overrides.

**Why this priority**: Currently every example entry duplicates metadata that already exists on the Route object. This creates drift (example says one model, Route says another) and is tedious. Eliminating the redundancy makes examples easier to write and impossible to get wrong.

**Independent Test**: Can be tested by adding an example entry with only `name` and `call`, then verifying the runner automatically discovers `response_model` and `fixture_file` from the Route.

**Acceptance Scenarios**:

1. **Given** an example entry with only a name and lambda, **When** the runner executes, **Then** it discovers the response model and fixture filename from the corresponding Route definition.
2. **Given** an example entry with an explicit `response_model` override, **When** the runner executes, **Then** the override takes precedence over auto-discovery.
3. **Given** a method with no matching Route (e.g., a helper method), **When** auto-discovery fails, **Then** the system falls back gracefully and runs without model metadata.

---

### User Story 3 - Upgraded Progress Tracking (Priority: P1)

A project lead opens `progress.html` and sees endpoints organized by path root (e.g., `/job`, `/contacts`, `/companies`) and tagged by domain. For each endpoint, the report shows: the HTTP method and path, the Python dotted method path (e.g., `api.jobs.get_timeline`), whether an example entry (`ex`) exists, and whether CLI commands (`ab`/`abs`) work. This gives a single-pane-of-glass view of SDK completeness.

**Why this priority**: Current progress tracking counts endpoints and quality gates but doesn't show the relationship between API routes, Python methods, example coverage, and CLI availability. The upgraded view answers "what can I use today?" at a glance.

**Independent Test**: Can be tested by running the progress generator and verifying the HTML output groups endpoints by path root, shows dotted Python paths, and has columns for `ex` and `ab`/`abs` availability.

**Acceptance Scenarios**:

1. **Given** the progress report is generated, **When** the user opens `progress.html`, **Then** endpoints are grouped by endpoint class (e.g., `jobs`) with sub-sections by path sub-root (e.g., `timeline`, `onhold`), using the same aliases as CLI and examples.
2. **Given** any endpoint row, **When** the user reads it, **Then** they see: HTTP method, raw path, Python dotted path, example status (has `ex` entry: yes/no), CLI status (`ab`/`abs` callable: yes/no).
3. **Given** the FIXTURES.md tracking file, **When** it is regenerated, **Then** each row includes the Python dotted method path alongside the HTTP path.
4. **Given** a method that has an example entry and CLI registration, **When** progress is rendered, **Then** both indicators show as available.

---

### User Story 4 - Method Listing with Discovery (Priority: P2)

A developer runs `ab jobs` (no method specified) and sees an enhanced listing: each method shows not just parameters but also the HTTP verb, raw URI, return type, and whether an example exists. Running `ab` alone lists all endpoint groups with method counts, aliases, and the path root they cover. No `--list` flag is ever required — a parent command with no arguments implicitly lists its children.

**Why this priority**: The current listing output shows method names and parameter signatures but nothing about the HTTP operation or return types. Enriching this output and making it implicit makes the CLI self-discoverable without opening docs.

**Independent Test**: Can be tested by running `ab jobs` and verifying each row includes the HTTP method, path, and return type alongside the Python method name.

**Acceptance Scenarios**:

1. **Given** an endpoint group, **When** the user runs `ab <group>` with no further arguments, **Then** each method shows: method name, HTTP verb, URI pattern, return type, and parameter summary.
2. **Given** the top-level command, **When** the user runs `ab` with no arguments, **Then** each endpoint group shows the count of methods, aliases, and the API path root it covers.
3. **Given** any level of the command hierarchy, **When** no child/method is specified, **Then** the listing is shown implicitly without requiring a `--list` flag.
4. **Given** an endpoint group with helper/composed methods (no Route), **When** the listing is shown, **Then** those methods appear in a "Helpers" section at the top, before Route-backed methods.

---

### User Story 5 - Sphinx & Docstring Alignment (Priority: P2)

A developer builds the Sphinx documentation and sees auto-generated API reference pages that include all the information from `--help`: URI, method signature, parameters, return type, and model cross-references. The Sphinx output and CLI `--help` output present the same information in different formats.

**Why this priority**: Documentation and CLI help currently diverge. Docstrings contain RST-style `:class:` references that render in Sphinx but appear as raw text in CLI output. Aligning the source data ensures consistency.

**Independent Test**: Can be tested by building Sphinx docs and verifying each endpoint method's auto-generated page includes the HTTP method, URI, parameters with types, return type, and clickable model links.

**Acceptance Scenarios**:

1. **Given** endpoint method docstrings, **When** Sphinx builds, **Then** each method page shows: HTTP verb and URI, parameter table, return type with model link.
2. **Given** a model referenced in a docstring, **When** the Sphinx docs are built, **Then** the model name is a clickable cross-reference to the model's documentation page.
3. **Given** the CLI `--help` output, **When** compared to the Sphinx page for the same method, **Then** the factual content (URI, params, return type) is identical.

---

### User Story 6 - Generic Constants & Fixture Discovery (Priority: P2)

A developer working on a new endpoint group needs test constants (e.g., `TEST_CONTACT_ID`) and the system automatically identifies which constants are needed based on the endpoint's URI path parameters. The progress report and action items suggest which constants to add when they're missing, without hardcoded mappings.

**Why this priority**: Currently, constants are manually mapped to endpoints. A new endpoint with `{companyId}` in its path should automatically know it needs a `TEST_COMPANY_ID` constant. Making this generic reduces boilerplate and catches missing test setup.

**Independent Test**: Can be tested by adding a new endpoint with a path parameter and verifying the progress system identifies the required constant by name pattern matching.

**Acceptance Scenarios**:

1. **Given** an endpoint with `{contactId}` in its path, **When** the progress system scans constants, **Then** it identifies `TEST_CONTACT_ID` or similar as a candidate constant.
2. **Given** a missing constant for a path parameter, **When** the progress report is generated, **Then** an action item is created suggesting the constant name and type.
3. **Given** fixtures exist for a model, **When** the progress system evaluates an endpoint, **Then** it discovers fixture files by model name without hardcoded filename mappings.

---

### Edge Cases

- Methods without a corresponding Route (helpers, composed wrappers like `get_timeline`) are shown in a "Helpers" section at the top of listings. They display Python signature but URI/return type are marked as unavailable.
- Methods that return `Any` (no typed response model on the Route) show the return type as `Any` in listings and `--help`.
- Multiple Routes sharing the same response model (e.g., `ServiceBaseResponse`) is not a problem — each method maps to its own Route independently.
- Methods with `**kwargs` or complex nested types display the raw annotation string in `--help`.
- Helper properties (e.g., `api.jobs.timeline`) that are not callable methods are excluded from method listings.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: CLI `--help` output for any endpoint method MUST display the raw API URI (e.g., `GET /job/{jobDisplayId}/timeline`)
- **FR-002**: CLI `--help` output MUST display the Python SDK call signature (e.g., `api.jobs.get_timeline(job_display_id: int) -> list[TimelineTask]`)
- **FR-003**: CLI `--help` output MUST display the CLI invocation syntax (e.g., `ab jobs get_timeline <job_display_id>`)
- **FR-004**: CLI `--help` output MUST display the return type from the Route's `response_model`
- **FR-005**: CLI `--help` output MUST display request model fields when the Route has a `request_model`
- **FR-006**: ExampleRunner MUST auto-discover `response_model` and `fixture_file` from the method's Route when not explicitly provided
- **FR-007**: ExampleRunner MUST auto-discover `request_model` and `request_fixture_file` from the method's Route when not explicitly provided
- **FR-008**: Progress report MUST group endpoints by endpoint class (e.g., `jobs`, `contacts`, `companies`) with sub-sections by path sub-root (e.g., `timeline`, `onhold`, `notes`)
- **FR-009**: Progress report rows MUST show the Python dotted method path (e.g., `api.jobs.get_timeline`)
- **FR-010**: Progress report rows MUST show example entry availability (`ex` column)
- **FR-011**: Progress report rows MUST show CLI availability (`ab`/`abs` column)
- **FR-012**: `ab <module>` (no method) MUST implicitly list methods showing HTTP verb, URI pattern, and return type — no `--list` flag required. Same for `ab` alone listing groups
- **FR-012a**: Method listings MUST show routeless methods (helpers, composed wrappers) in a separate "Helpers" section at the top, before Route-backed methods
- **FR-013**: The alias registry MUST be shared as a single source across CLI (`ab`/`abs`), examples (`ex`), and progress report — no separate alias definitions per tool
- **FR-014**: Constant discovery MUST infer required test constants from URI path parameter names
- **FR-015**: Fixture discovery MUST resolve fixture files by Route model name without hardcoded mappings
- **FR-016**: Endpoint docstrings MUST follow a structured format that serves both Sphinx rendering and CLI `--help` display
- **FR-017**: Sphinx documentation MUST auto-generate method reference pages with URI, parameters, return type, and model cross-references

### Key Entities

- **Route**: Existing immutable dataclass — the single source of truth for URI, method, request model, response model, and params model. All discovery derives from this.
- **MethodInfo**: CLI discovery dataclass — extended to include Route metadata (URI, response model) alongside parameter signatures.
- **ExampleEntry**: Example runner dataclass — extended to support auto-populated model metadata from Route discovery.
- **EndpointProgress**: New concept — a unified view of an endpoint combining Route, Python method, example entry, CLI availability, and quality gate status.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `--help` on any endpoint method shows the raw URI, Python signature, CLI syntax, and return type — verified for at least 10 methods across 3 endpoint groups
- **SC-002**: At least 80% of existing example entries can remove explicit `response_model` and `fixture_file` arguments and still function correctly via auto-discovery
- **SC-003**: Progress report groups endpoints by endpoint class with sub-sections, showing at least 5 distinct endpoint groups
- **SC-004**: Every progress report row shows Python dotted path, `ex` status, and `ab`/`abs` status
- **SC-005**: Sphinx-generated docs for each endpoint method include URI, parameter table, and return type with model cross-reference
- **SC-006**: `ab <module>` output (implicit listing) includes HTTP verb, URI, and return type for every method — verified for all endpoint groups

## Assumptions

- Route objects remain the single source of truth for endpoint metadata. No new metadata storage is introduced.
- The CLI `--help` can extract Route information by matching method names to module-level `_UPPERCASE` Route constants via naming convention or docstring parsing.
- Sphinx continues using `sphinx.ext.autodoc` with the existing `sphinx-rtd-theme`. No theme change is planned.
- The progress report HTML is generated by `scripts/generate_progress.py` and the infrastructure in `ab/progress/`. The existing G1-G6 quality gates are retained and extended, not replaced.
- Path parameter-to-constant matching uses a naming convention (e.g., `{contactId}` maps to `TEST_CONTACT_ID`) rather than explicit configuration.
- The `ex` console script and `ab`/`abs` console scripts continue to be separate entry points with shared discovery infrastructure and a single shared alias registry.
