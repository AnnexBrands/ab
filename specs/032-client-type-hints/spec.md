# Feature Specification: Client Endpoint Type Hints for IDE Discoverability

**Feature Branch**: `032-client-type-hints`
**Created**: 2026-03-08
**Status**: Draft
**Input**: User description: "Add type hints for all endpoints in client.py. Ensure sphinx and CLI help and examples are kept current"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - IDE Autocompletion on Endpoint Methods (Priority: P1)

A developer types `api = ABConnectAPI()` then `api.dashboard.` and presses Ctrl+Space. The IDE displays all available methods on the dashboard endpoint (e.g., `get`, `inbound`, `outbound`, `in_house`, `local_deliveries`, `recent_estimates`, `get_grid_views`, `get_grid_view_state`, `save_grid_view_state`) with their signatures and docstrings. This works for every endpoint attribute on the client.

**Why this priority**: This is the core problem — without type annotations on the client's endpoint attributes, IDE tooling cannot infer the types and users get no autocompletion or signature help. This is the single change that unblocks all other IDE discoverability.

**Independent Test**: Can be verified by opening a Python file in an IDE (PyCharm, VS Code with Pylance), typing `api.dashboard.` and confirming method suggestions appear with correct signatures and return types.

**Acceptance Scenarios**:

1. **Given** a developer has imported and instantiated `ABConnectAPI`, **When** they type `api.` and trigger autocomplete, **Then** all endpoint attributes (companies, contacts, jobs, dashboard, etc.) appear with their correct types.
2. **Given** a developer has accessed an endpoint attribute (e.g., `api.dashboard.`), **When** they trigger autocomplete, **Then** all methods on that endpoint appear with parameter names, types, and return types.
3. **Given** a developer has navigated to a method parameter typed with a request model (e.g., `data: DashboardCompanyRequest`), **When** they trigger autocomplete on the model, **Then** the model's fields and their types are visible.

---

### User Story 2 - Request Model Discoverability (Priority: P2)

After discovering the method signature via autocomplete, a developer can jump to the definition of request/response models (e.g., `DashboardCompanyRequest`) and see all available fields with descriptions. The developer can construct request data with field-level autocomplete.

**Why this priority**: Type hints on the client enable method discovery, but the developer also needs to build request payloads. The request models already have full Pydantic field definitions — the type hints on the client are the missing link that lets IDEs trace from `api.dashboard.inbound(data=...)` to the `DashboardCompanyRequest` model.

**Independent Test**: Can be verified by hovering over or go-to-definition on a `data` parameter in an endpoint method call, confirming the IDE resolves to the correct Pydantic model with all fields visible.

**Acceptance Scenarios**:

1. **Given** a developer is calling `api.dashboard.inbound(data=...)`, **When** they hover over the `data` parameter, **Then** the IDE shows the type as `DashboardCompanyRequest | dict` with the model's docstring.
2. **Given** a developer constructs `DashboardCompanyRequest(`, **When** they trigger autocomplete, **Then** all fields (e.g., `company_id`) appear with their types and descriptions.

---

### User Story 3 - Documentation and CLI Remain Accurate (Priority: P2)

After the type hint changes, Sphinx autodoc still generates correct API reference documentation, CLI `--list` and `--help` still display all endpoints and methods, and all examples continue to run.

**Why this priority**: Type annotations are an additive change, but regressions in docs, CLI discovery, or examples would break the existing developer experience. Verification is essential.

**Independent Test**: Run Sphinx build and confirm no warnings/errors. Run `ab --list` and `ab dashboard --help` and confirm output. Run `ex --list` and confirm all examples are listed.

**Acceptance Scenarios**:

1. **Given** Sphinx docs are built after the change, **When** a user views the API reference for `ABConnectAPI`, **Then** all endpoint attributes are documented with their types.
2. **Given** a user runs `ab --list`, **When** the output is displayed, **Then** all endpoints appear with their methods, unchanged from before.
3. **Given** a user runs `ab dashboard --help`, **When** the output is displayed, **Then** all dashboard methods and their parameters are shown correctly.

---

### Edge Cases

- Backward-compatible aliases (`self.docs = self.documents`, `self.cmaps = self.commodity_maps`) must also have type annotations so IDE discoverability works through aliases.
- Endpoints with multiple HTTP client dependencies (e.g., `JobsEndpoint` takes `_acportal`, `_abc`, and `_resolver`) must not have their constructor signatures affected.
- The `py.typed` marker file already exists — no additional PEP 561 work is needed.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every endpoint attribute on `ABConnectAPI` MUST have an explicit type annotation matching its assigned endpoint class (e.g., `self.dashboard: DashboardEndpoint = ...`).
- **FR-002**: Backward-compatible alias attributes (`docs`, `cmaps`) MUST have type annotations matching their target endpoint types.
- **FR-003**: The type annotations MUST be resolvable by standard Python type checkers (mypy, pyright/Pylance) without `TYPE_CHECKING` guards, since these are runtime assignments on an instantiated class.
- **FR-004**: Sphinx autodoc output MUST continue to build without errors or regressions after the change.
- **FR-005**: CLI discovery (`--list`, `--help`) MUST produce identical output before and after the change.
- **FR-006**: All existing examples MUST continue to function without modification.
- **FR-007**: All existing tests MUST continue to pass without modification.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer typing `api.<endpoint>.` in a supported IDE (VS Code with Pylance, PyCharm) sees method completions for all 22 endpoint groups.
- **SC-002**: Sphinx documentation builds with zero new warnings or errors.
- **SC-003**: CLI `--list` output is identical before and after the change.
- **SC-004**: All existing unit tests pass without modification.
- **SC-005**: A type checker reports no new type errors introduced by the change.

## Assumptions

- The `py.typed` marker already exists, so the package is already recognized as PEP 561 compliant.
- Endpoint classes are already fully importable at runtime (not behind `TYPE_CHECKING` guards in `ab/api/endpoints/__init__.py`).
- The change is purely additive — no behavioral changes to any endpoint, model, CLI, or documentation logic.
