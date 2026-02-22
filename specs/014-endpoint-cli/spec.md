# Feature Specification: Endpoint CLI

**Feature Branch**: `014-endpoint-cli`
**Created**: 2026-02-22
**Status**: Draft
**Input**: User description: "review progress, attempt to resolve failures in progress.html. check that sphinx, examples, and test are complete. begin the implementation of a new cli. we have ex but need endpoint calls. it should be abs for ABConnectAPI(env='staging') and ab for no env aka prod. I should be able to call ab addr isvalid just like ex addr isvalid."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Call an Endpoint from the Command Line (Priority: P1)

A developer wants to quickly call any ABConnect API endpoint from the terminal without writing Python code. They type `ab addr validate` (production) or `abs addr validate` (staging) and see the JSON response printed to stdout. The command names, aliases, and prefix matching work identically to the existing `ex` CLI.

**Why this priority**: This is the core value proposition — replacing the need to write one-off scripts for every API call. Without this, the other stories have no foundation.

**Independent Test**: Can be fully tested by running `abs addr validate --line1="12742 E Caley Av" --city=Centennial --state=CO --zip=80111` and verifying a JSON response is printed.

**Acceptance Scenarios**:

1. **Given** the SDK is installed, **When** the user runs `ab addr validate --line1="123 Main St" --city=Denver --state=CO --zip=80202`, **Then** the CLI prints the JSON response from the production API.
2. **Given** the SDK is installed, **When** the user runs `abs addr validate --line1="123 Main St" --city=Denver --state=CO --zip=80202`, **Then** the CLI connects to the staging environment and prints the JSON response.
3. **Given** the SDK is installed, **When** the user runs `ab --list`, **Then** all available endpoint groups are listed with method counts and aliases (same aliases as `ex`).
4. **Given** the SDK is installed, **When** the user runs `ab companies --list`, **Then** all methods for the companies endpoint are listed with their parameter signatures.
5. **Given** the user types an ambiguous prefix, **When** multiple endpoints match, **Then** the CLI lists the matching options and exits with a nonzero status (same behavior as `ex`).

---

### User Story 2 - Discover Endpoint Methods and Parameters (Priority: P2)

A developer wants to explore what methods are available on an endpoint and what parameters each method accepts, without reading source code. They use `--list` and `--help` to discover this information.

**Why this priority**: Discovery is essential for usability — without it, users must read source code to know what parameters to pass. This makes the CLI self-documenting.

**Independent Test**: Can be tested by running `ab jobs --list` and verifying all public methods are shown with parameter names and types.

**Acceptance Scenarios**:

1. **Given** the SDK is installed, **When** the user runs `ab jobs --list`, **Then** all public methods on the jobs endpoint are listed with their parameter names.
2. **Given** the SDK is installed, **When** the user runs `ab addr validate --help`, **Then** the method's parameters, their types, and defaults are displayed.

---

### User Story 3 - Parity with `ex` CLI Interaction Model (Priority: P2)

A developer already familiar with the `ex` CLI expects the same interaction patterns: dot syntax (`ab addr.validate`), space syntax (`ab addr validate`), aliases (`ab co` → companies), and prefix matching (`ab addr val` → `ab addr validate`).

**Why this priority**: Consistency reduces learning curve. The `ex` CLI patterns are already established and expected.

**Independent Test**: Can be tested by running `ab co.get_by_id --company-id=<uuid>` and `ab companies get_by_id --company-id=<uuid>` and verifying both produce the same result.

**Acceptance Scenarios**:

1. **Given** the CLI is installed, **When** the user runs `ab addr.validate --line1=X`, **Then** the result is identical to `ab addr validate --line1=X`.
2. **Given** the CLI is installed, **When** the user runs `ab co`, **Then** it resolves to the companies endpoint (same alias mapping as `ex`).
3. **Given** the CLI is installed, **When** the user runs `ab addr val`, **Then** it resolves to `validate` via prefix matching.

---

### User Story 4 - Review Progress and Resolve Gate Failures (Priority: P3)

Before implementing new features, the project maintainer wants to review current SDK quality status, resolve any addressable gate failures in the progress report, and ensure Sphinx docs, examples, and tests are in a consistent state.

**Why this priority**: Housekeeping ensures the baseline is clean before adding new functionality. This is lower priority because the test suite already passes (232/0/73).

**Independent Test**: Can be tested by running `python scripts/generate_progress.py` and verifying the report generates without errors, then checking that `pytest`, `ruff check .`, and `cd docs && make html` all pass.

**Acceptance Scenarios**:

1. **Given** the current codebase, **When** the progress report is generated, **Then** it reflects the current gate status accurately and any addressable failures are resolved.
2. **Given** the current codebase, **When** `pytest --tb=short -q` is run, **Then** all tests pass with 0 failures.
3. **Given** the current codebase, **When** `cd docs && make html` is run, **Then** the build succeeds (warnings are acceptable, errors are not).

---

### Edge Cases

- What happens when the user calls an endpoint method that requires authentication but credentials are not configured? The CLI displays a clear error message indicating which environment file is missing or which credentials are invalid.
- What happens when the user passes an argument that doesn't match any method parameter? The CLI rejects unknown arguments with a helpful message showing valid parameters.
- What happens when the API returns an error (4xx, 5xx)? The CLI displays the HTTP status code and response body, then exits with a nonzero status.
- What happens when the user passes no arguments to a method that requires them? The CLI shows the method signature and required parameters.
- How does the CLI handle methods with complex parameter types (e.g., nested objects, lists)? For POST/PUT endpoints that require a request body, the CLI accepts JSON via `--body` or stdin.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide two console-script entry points: `ab` (production) and `abs` (staging), where each creates `ABConnectAPI()` and `ABConnectAPI(env="staging")` respectively.
- **FR-002**: System MUST reuse the same module aliases defined for the `ex` CLI (e.g., `addr`→`address`, `co`→`companies`, `ct`→`contacts`).
- **FR-003**: System MUST support three dispatch syntaxes: dot syntax (`ab module.method`), space syntax (`ab module method`), and bare module (`ab module` → list methods).
- **FR-004**: System MUST support prefix matching for both module names and method names, with ambiguity resolution identical to the `ex` CLI.
- **FR-005**: System MUST pass CLI arguments as keyword arguments to endpoint methods, mapping `--param-name=value` to the corresponding Python parameter.
- **FR-006**: System MUST discover endpoint methods dynamically by introspecting the `ABConnectAPI` instance's endpoint attributes and their public methods.
- **FR-007**: System MUST print JSON responses to stdout, formatted for readability.
- **FR-008**: System MUST exit with status 0 on success and nonzero on failure (ambiguity, unknown endpoint, API error, missing credentials).
- **FR-009**: System MUST provide `--list` at both the top level (list all endpoint groups) and module level (list all methods in a group).
- **FR-010**: Progress report (`progress.html`) MUST be regenerated with current gate evaluations. Any addressable gate failures should be resolved where feasible.

### Key Entities

- **Endpoint Group**: A named collection of methods corresponding to one API surface (e.g., "address", "companies"). Mapped 1:1 to endpoint classes on the ABConnectAPI client.
- **Method**: A single callable operation within an endpoint group (e.g., `validate`, `get_by_id`). Has a name, parameter signature, and route metadata.
- **Alias**: A shorthand name for an endpoint group (e.g., `addr` → `address`). Shared with the `ex` CLI.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `abs addr validate --line1="12742 E Caley Av" --city=Centennial --state=CO --zip=80111` prints a valid JSON response within 5 seconds.
- **SC-002**: `ab --list` displays all endpoint groups (matching the count from `ex --list`) with method counts and aliases.
- **SC-003**: All existing tests continue to pass (232 passed, 0 failures) and `ruff check .` reports no issues.
- **SC-004**: Sphinx documentation builds successfully (`make html` in `docs/`).
- **SC-005**: The `ab` and `abs` entry points are registered and functional after installation.
- **SC-006**: Every endpoint method discoverable via `ex` is also callable via `ab`/`abs` using the same alias and method name.

## Assumptions

- The `ab` and `abs` command names do not conflict with existing system commands on the target platforms. The user has confirmed these names.
- Authentication credentials are pre-configured in `.env` (production) and `.env.staging` (staging) files — the CLI does not implement credential setup, only uses existing SDK authentication.
- Complex request bodies (POST/PUT) are passed as JSON strings via `--body` or piped from stdin. Individual field-level arguments for request bodies are out of scope for the initial implementation.
- The progress report review (US4) is a one-time housekeeping task scoped to this feature branch, not an ongoing automated process.
