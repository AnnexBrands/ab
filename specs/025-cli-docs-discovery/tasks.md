# Tasks: CLI Docs & Discovery Major Release

**Input**: Design documents from `/specs/025-cli-docs-discovery/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-help-format.md, quickstart.md

**Tests**: Not explicitly requested — verification included in Polish phase.

**Organization**: Tasks grouped by user story (6 stories: US1–US3 are P1, US4–US6 are P2).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No new project initialization needed — existing SDK. Ensure branch is clean.

- [x] T001 Verify branch `025-cli-docs-discovery` is checked out and working tree is clean via `git status`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that ALL user stories depend on — RouteResolver and extended MethodInfo/EndpointInfo.

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T002 Create `ab/cli/route_resolver.py` — implement `resolve_routes_for_class(cls) -> dict[str, Route]` that introspects each public method's source code via `inspect.getsource()`, finds `self._request(_ROUTE_NAME` references via regex `r'(?:self\._request|_request)\(\s*(_[A-Z_][A-Z0-9_]*)'`, matches them to module-level `Route` instances found via `isinstance(obj, Route)` check on `inspect.getmodule(cls)`, and returns a `{method_name: Route}` dict. Also implement `path_param_to_constant(param: str) -> str` that converts camelCase path param names to `TEST_SCREAMING_SNAKE` format via `re.sub(r'([A-Z])', r'_\1', param).upper()`. Import `Route` from `ab.api.route` and `inspect`, `re` from stdlib.

- [x] T003 Extend `MethodInfo` dataclass in `ab/cli/discovery.py` — add two new fields: `route: Route | None = None` (import `Route` from `ab.api.route`) and `return_annotation: str | None = None`. In `_extract_methods()`, after creating each `MethodInfo`, attempt to capture the return annotation from the method signature via `sig.return_annotation` (convert to string representation, skip if `inspect.Parameter.empty`). The `route` field will be populated by the caller after method extraction.

- [x] T004 Extend `EndpointInfo` dataclass in `ab/cli/discovery.py` — add two new fields: `aliases: list[str] = field(default_factory=list)` and `path_root: str | None = None`. In `discover_endpoints_from_class()`, after building the endpoint dict, import `ALIASES` from `ab.cli.aliases` and populate `aliases` by building a reverse alias map. Populate `path_root` by calling `resolve_routes_for_class(cls)` (import from `ab.cli.route_resolver`), collecting all Route paths, and extracting the common first path segment (e.g., `/job` from `/job/{id}`, `/job/{id}/timeline`). Also populate each `MethodInfo.route` from the resolved routes dict.

**Checkpoint**: Foundation ready — `resolve_routes_for_class()` returns method→Route mappings, `MethodInfo` carries Route metadata, `EndpointInfo` carries aliases and path root. User story implementation can begin.

---

## Phase 3: User Story 1 — Rich CLI Help for Any Endpoint (Priority: P1) MVP

**Goal**: `ab <module> <method> --help` displays a complete reference card: raw URI, Python signature, CLI syntax, params with types/defaults, return type, and model fields.

**Independent Test**: Run `ab jobs get --help` and verify output contains `GET /job/{jobDisplayId}`, `api.jobs.get(job_display_id: int) -> Job`, `ab jobs get <job_display_id>`, and `Returns: Job`.

### Implementation for User Story 1

- [x] T005 [US1] Add a `_strip_rst(text: str) -> str` helper function in `ab/cli/parser.py` that removes RST `:class:`, `:meth:`, `:func:`, `:attr:` role markup from docstrings, converting `:class:\`ModelName\`` to plain `ModelName`. Use `re.sub(r':\w+:`([^`]+)`', r'\1', text)`.

- [x] T006 [US1] Add a `_format_python_signature(module_name: str, method: MethodInfo) -> str` helper in `ab/cli/parser.py` that builds the full Python call signature string like `api.jobs.get(job_display_id: int) -> Job`. Iterate `method.positional_params` and `method.keyword_params`, format each with type annotation and default value. Append `-> {method.return_annotation}` if available, falling back to the Route's `response_model` if set.

- [x] T007 [US1] Add a `_format_cli_syntax(module_name: str, method: MethodInfo) -> str` helper in `ab/cli/parser.py` that builds the CLI invocation string like `ab jobs get <job_display_id> [--flag=VALUE]`. Use `<name>` for positional args and `[--flag=VALUE]` for optional keyword args.

- [x] T008 [US1] Add a `_format_model_fields(model_name: str, max_fields: int = 10) -> list[str]` helper in `ab/cli/parser.py` that imports `ab.api.models`, resolves the model class via `getattr`, iterates `model_cls.model_fields`, and returns formatted lines like `  fieldName       type       description`. Handle `List[Model]` by parsing inner name. Return empty list if model not found or not a Pydantic BaseModel.

- [x] T009 [US1] Rewrite `print_method_help(method: MethodInfo, module_name: str = "")` in `ab/cli/parser.py` to output the structured reference card format defined in `contracts/cli-help-format.md`. Display: method name with underline, first paragraph of docstring (RST-stripped), Route line (`{method} {path}`) if `method.route` exists, Python signature line, CLI syntax line, Returns line, positional/keyword argument sections, and response/request/params model field sections (show each only when the Route has the corresponding model set: `response_model`, `request_model`, `params_model`). Accept `module_name` parameter for building dotted paths. Print all to stderr.

- [x] T010 [US1] Update the `--help` call site in `ab/cli/__main__.py` (around line 225-229) to pass `module_name=mod_name` when calling `print_method_help(method, module_name=mod_name)` so the help card can build the correct dotted path and CLI syntax.

**Checkpoint**: `ab jobs get --help` shows the full reference card with URI, Python signature, CLI syntax, return type. No credentials needed.

---

## Phase 4: User Story 2 — Route-Derived Model Discovery (Priority: P1)

**Goal**: `ExampleRunner.add()` auto-discovers `response_model`, `fixture_file`, `request_model`, `request_fixture_file` from the Route when not explicitly provided.

**Independent Test**: Create an ExampleRunner entry with only `name` and `call`, verify `entry.response_model` and `entry.fixture_file` are auto-populated.

### Implementation for User Story 2

- [x] T011 [US2] Add an `endpoint_attr: str | None = None` parameter to `ExampleRunner.__init__()` in `examples/_runner.py`. Store it as `self.endpoint_attr`. Add a lazy-initialized `self._method_routes: dict[str, Route] | None = None` field.

- [x] T012 [US2] Add a `_resolve_method_routes(self) -> dict[str, Route]` method to `ExampleRunner` in `examples/_runner.py`. If `self.endpoint_attr` is None, return `{}`. Otherwise, use `discover_endpoints_from_class()` (import from `ab.cli.discovery`) to get the endpoint registry, find the matching endpoint class by `self.endpoint_attr`, then call `resolve_routes_for_class(cls)` (import from `ab.cli.route_resolver`) to get the method→Route mapping. Cache the result in `self._method_routes`.

- [x] T013 [US2] Add a `_auto_populate_entry(self, entry: ExampleEntry) -> None` method to `ExampleRunner` in `examples/_runner.py`. If `entry.response_model` is not None and `entry.fixture_file` is not None, return early (explicit override). Otherwise, call `self._resolve_method_routes()` to get routes, look up `entry.name` in the dict. If found: (a) if `entry.response_model is None` and route has `response_model`, parse `List[X]` to extract inner name via regex `r'^List\[(\w+)\]$'`, set `entry.response_model` to the model name; (b) if `entry.fixture_file is None` and `entry.response_model` is set, set `entry.fixture_file = f"{entry.response_model}.json"`; (c) similarly for `request_model` and `request_fixture_file` from route's `request_model`.

- [x] T014 [US2] Call `self._auto_populate_entry(entry)` at the end of `ExampleRunner.add()` in `examples/_runner.py`, right after the entry is appended to `self.entries`. This ensures auto-discovery runs at registration time.

- [x] T015 [US2] Update one example file (`examples/jobs.py`) to add `endpoint_attr="jobs"` to the `ExampleRunner(...)` constructor call, and remove explicit `response_model` and `fixture_file` from 3-5 entries (e.g., `get`, `get_price`, `get_calendar_items`) to verify auto-discovery works. Keep remaining entries unchanged to validate that explicit overrides still take precedence.

**Checkpoint**: ExampleRunner auto-populates model metadata from Routes. Existing explicit values still override. Run `python -m examples jobs --list` to verify auto-populated entries show correct models.

---

## Phase 5: User Story 3 — Upgraded Progress Tracking (Priority: P1)

**Goal**: Progress report groups endpoints by endpoint class with sub-sections by path sub-root. Each row shows Python dotted path, example status (`ex`), and CLI status (`ab`/`abs`).

**Independent Test**: Run `python scripts/generate_progress.py` and verify `html/progress.html` groups by endpoint class, shows dotted paths, and has `ex`/`ab` columns.

### Implementation for User Story 3

- [x] T016 [P] [US3] Add `MethodProgress` and `EndpointClassProgress` dataclasses to `ab/progress/models.py` per the data-model.md definitions. `MethodProgress` has: `dotted_path: str`, `method_name: str`, `http_method: str`, `http_path: str`, `return_type: str`, `has_example: bool`, `has_cli: bool`, `has_route: bool`, `path_sub_root: str`, `gate_status: EndpointGateStatus | None = None`. `EndpointClassProgress` has: `class_name: str`, `display_name: str`, `aliases: list[str]`, `path_root: str`, `helpers: list[MethodProgress]`, `sub_groups: dict[str, list[MethodProgress]]`, `total_methods: int = 0`, `total_with_route: int = 0`, `total_with_example: int = 0`, `total_with_cli: int = 0`. Import `EndpointGateStatus` from `ab.progress.gates`.

- [x] T017 [P] [US3] Add a `build_endpoint_class_progress() -> list[EndpointClassProgress]` function in `ab/progress/route_index.py`. Import `discover_endpoints_from_class` from `ab.cli.discovery`, `ALIASES` from `ab.cli.aliases`. For each endpoint in the discovery registry: build `MethodProgress` entries from each method's `MethodInfo` (using `method.route` for HTTP details, marking `has_route=False` for routeless helpers, setting `has_cli=True` for all discovered methods since all are CLI-callable). Extract `path_sub_root` by taking the first path segment after the second `{param}` or after the base path root. Group methods: routeless ones go to `helpers`, routed ones go to `sub_groups` keyed by sub-root. Populate aliases from `ALIASES` reverse map. Compute totals.

- [x] T018 [US3] Add `_scan_example_entries() -> dict[str, set[str]]` helper in `ab/progress/route_index.py` that scans `examples/*.py` files to discover which methods have example entries. For each example module, import it and check for a `runner` attribute, then iterate `runner.entries` to collect `{endpoint_attr: {entry.name, ...}}`. Use the result to set `has_example=True` on matching `MethodProgress` entries in `build_endpoint_class_progress()`.

- [x] T019 [US3] Add `render_endpoint_class_progress(progress: list[EndpointClassProgress]) -> str` function in `ab/progress/renderer.py`. Render an HTML section with `<h2>Endpoint Coverage by Class</h2>`. For each `EndpointClassProgress`: render `<h3>{class_name}</h3>` with method count and aliases. If `helpers` exist, render a "Helpers" table with columns: Method, Python Path, Ex, CLI. For each `sub_group`, render a sub-table with columns: HTTP, Path, Method, Python Path, Return, Ex, CLI. Use existing CSS classes (`badge-done`, `badge-ns`) for yes/no indicators. Gate columns are optional in this view.

- [x] T020 [US3] Update `render_report()` in `ab/progress/renderer.py` to accept an optional `endpoint_class_progress: list[EndpointClassProgress] | None = None` parameter. If provided, insert the `render_endpoint_class_progress()` output after the summary section and before the gate details.

- [x] T021 [US3] Update `scripts/generate_progress.py` to call `build_endpoint_class_progress()` (import from `ab.progress.route_index`) and pass the result to `render_report()` via the new `endpoint_class_progress` parameter. Ensure the progress report is written to `html/progress.html` with the new grouped view.

- [x] T022 [US3] Add a "Python Path" column to `generate_fixtures_md()` in `ab/progress/fixtures_generator.py`. For each endpoint row, resolve the Python dotted method path by matching the row's `(endpoint_path, method)` to the `build_endpoint_class_progress()` output. Update the table header to include `Python Path` between `Method` and `Req Model` columns. Update each row to include the dotted path (e.g., `api.jobs.get_timeline`) or `—` if no matching method is found. This satisfies US3 acceptance scenario 3 (FIXTURES.md includes dotted method path).

**Checkpoint**: `python scripts/generate_progress.py` produces `html/progress.html` with endpoint-class grouping, dotted paths, and ex/ab columns. FIXTURES.md includes Python dotted paths.

---

## Phase 6: User Story 4 — Method Listing with Discovery (Priority: P2)

**Goal**: `ab <module>` implicitly lists methods showing HTTP verb, URI, return type. `ab` alone lists groups with method counts, path root, and aliases. Helpers shown first in a separate section. No `--list` flag needed.

**Independent Test**: Run `ab jobs` and verify output shows HTTP method, path, return type for each method, with helpers at top.

### Implementation for User Story 4

- [x] T023 [US4] Rewrite `_list_methods(endpoint: EndpointInfo)` in `ab/cli/__main__.py` to display the enriched listing format from `contracts/cli-help-format.md`. Separate methods into two groups: helpers (where `m.route is None`) and API methods (where `m.route is not None`). For helpers, show a "Helpers (no API route)" section with method name and parameter summary. For API methods, show each row as `{HTTP} {path}   {method}({params}) -> {return_type}`. Sort API methods by Route path. Use the extended `MethodInfo.route` and `MethodInfo.return_annotation` fields.

- [x] T024 [US4] Rewrite `_list_all(registry: dict[str, EndpointInfo])` in `ab/cli/__main__.py` to add "Path Root" and "Aliases" columns (Path Root from `EndpointInfo.path_root`, Aliases from `EndpointInfo.aliases`). Format: `{name:<20} {count:>7}   {path_root:<15}   {aliases}`.

- [x] T025 [US4] Simplify the dispatch logic in `main()` in `ab/cli/__main__.py`: remove the explicit `rest == ["--list"]` check on line 203 (the `if method_part is None and (not rest or rest == ["--list"])` block). Make listing the default when no method is specified — `ab <module>` (with or without `--list`) shows the enriched listing. Similarly, ensure top-level `ab` (line 177) handles both `not args` and `args == ["--list"]` identically (already does, just clean up the docstring comment).

**Checkpoint**: `ab jobs` shows enriched listing with HTTP verbs, paths, return types, and helpers at top. `ab` shows groups with path roots and aliases.

---

## Phase 7: User Story 5 — Sphinx & Docstring Alignment (Priority: P2)

**Goal**: Sphinx auto-generated pages show the same factual content as `--help`: URI, parameters, return type, model cross-references.

**Independent Test**: Run `cd docs && make html` and verify each endpoint method page includes HTTP method, URI, parameter table, and clickable model links.

### Implementation for User Story 5

- [x] T026 [P] [US5] Update 3 representative endpoint method docstrings to a consistent structured format. In `ab/api/endpoints/jobs.py`, update docstrings for `get()`, `get_timeline()`, and `create_timeline_task()` to follow this pattern: first line is `{HTTP_METHOD} {path}` (already the convention), then a blank line, then a description paragraph, then an `Args:` section, then a `Returns:` line with `:class:\`ModelName\`` reference, then a `Route:` line showing the Route constant name. This establishes the docstring convention for the rest of the codebase.

- [x] T027 [P] [US5] Create or update `docs/api/endpoints.rst` (or `.md` if using MyST) to use `.. automodule:: ab.api.endpoints.jobs` with `:members:` and `:undoc-members:` directives for each endpoint module. Ensure the Sphinx `autodoc` config in `docs/conf.py` has `autodoc_typehints = "description"` (already set) and `autodoc_default_options = {"members": True, "show-inheritance": True}`. If `docs/api/` directory doesn't exist, create it with an `index.rst` that includes each endpoint module.

- [x] T028 [US5] Verify Sphinx builds without warnings by running `cd docs && make html 2>&1`. Fix any broken `:class:` cross-references by ensuring model classes are importable via `ab.api.models`. If models are missing from `ab/api/models/__init__.py` re-exports, add them.

**Checkpoint**: `make html` succeeds. Each endpoint method page shows URI, params, return type, and model links.

---

## Phase 8: User Story 6 — Generic Constants & Fixture Discovery (Priority: P2)

**Goal**: Progress system infers required test constants from URI path parameter names. Fixture files are resolved by model name without hardcoded mappings.

**Independent Test**: Verify `path_param_to_constant("contactId")` returns `"TEST_CONTACT_ID"`. Verify progress report shows missing constant action items.

### Implementation for User Story 6

- [x] T029 [US6] Refactor `detect_required_constants()` in `ab/progress/instructions.py` to use the generic `path_param_to_constant()` from `ab/cli/route_resolver.py` instead of any hardcoded mappings. The function should: extract `{paramName}` placeholders from the endpoint path via `re.findall(r'\{([^}]+)\}', path)`, convert each to `TEST_SCREAMING_SNAKE` via `path_param_to_constant()`, and return the list of required constant names.

- [x] T030 [US6] Update `classify_action_items()` in `ab/progress/models.py` to use the generic fixture resolution: when checking `fixture_exists`, resolve fixture file name from `ep.response_model` as `f"{ep.response_model}.json"` and check if that file exists in `tests/fixtures/`. Remove any hardcoded fixture filename mappings if present.

- [x] T031 [US6] Verify the generic discovery works end-to-end by running `python scripts/generate_progress.py` and confirming that action items for endpoints with `{contactId}`, `{companyId}`, etc. in their paths correctly identify `TEST_CONTACT_ID`, `TEST_COMPANY_ID` as required constants. Check the HTML output for correct "Needs Constant" badges.

**Checkpoint**: Constants and fixtures are discovered generically from Route metadata. No hardcoded mappings.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Verification, cleanup, and cross-cutting improvements.

- [x] T032 [P] Write unit tests for `resolve_routes_for_class()` in `tests/unit/test_route_resolver.py` — test against `ContactsEndpoint` (known Routes), verify correct method→Route mapping, verify helper methods return no Route, verify `path_param_to_constant()` conversion for `jobDisplayId`, `contactId`, `companyId`, `id`.

- [x] T033 [P] Write CLI output integration tests in `tests/unit/test_cli_output.py` — test `print_method_help()` output contains expected strings (URI, Python signature, CLI syntax, params model fields), test `_list_methods()` output format, test `_list_all()` output format. Use `io.StringIO` or `capsys` to capture stderr output.

- [x] T034 Run quickstart.md smoke test checklist — execute all 7 verification scenarios from `specs/025-cli-docs-discovery/quickstart.md` and verify all assertions pass.

- [x] T035 Run `ruff check .` and fix any lint violations introduced by this feature. Ensure no new line-length, unused import, or import ordering violations.

- [x] T036 Run `pytest` to ensure no existing tests are broken by the changes. All existing model, integration, and parameter tests must still pass.

- [x] T037 Update `FIXTURES.md` by running `python scripts/generate_progress.py --fixtures` to regenerate with the new Python Path column and any other data from the upgraded progress system.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — immediate.
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories.
  - T002 (RouteResolver) must complete before T003/T004.
  - T003 (MethodInfo extension) and T004 (EndpointInfo extension + route population) are sequential (T004 depends on T003).
- **US1–US3 (Phases 3–5, all P1)**: All depend on Phase 2 completion. Can proceed in parallel.
- **US4 (Phase 6, P2)**: Depends on Phase 2. Can run in parallel with US1–US3.
- **US5 (Phase 7, P2)**: Depends on Phase 2. Best done after US1 (docstring format established).
- **US6 (Phase 8, P2)**: Depends on Phase 2. Can run in parallel with all others.
- **Polish (Phase 9)**: Depends on all user stories being complete.

### User Story Dependencies

- **US1 (Rich Help)**: Phase 2 only. No dependency on other stories.
- **US2 (Auto-Discovery)**: Phase 2 only. No dependency on other stories.
- **US3 (Progress)**: Phase 2 only. No dependency on other stories.
- **US4 (Listings)**: Phase 2 only. Shares `MethodInfo`/`EndpointInfo` with US1 (no conflict — different functions).
- **US5 (Sphinx)**: Phase 2. Benefits from US1's docstring format but can proceed independently.
- **US6 (Constants)**: Phase 2 only. No dependency on other stories.

### Within Each User Story

- Models/dataclasses before services/functions
- Core implementation before integration
- Each story independently verifiable at its checkpoint

### Parallel Opportunities

- **Phase 2**: T003 and T004 are sequential (T004 uses T003's changes).
- **Phase 3–5**: US1, US2, US3 can all run in parallel (different files).
- **Phase 6–8**: US4, US5, US6 can all run in parallel (different files).
- **Within US1**: T005–T008 (helper functions) add separate functions to same file — sequential execution preferred to avoid merge conflicts; T009 depends on all of them.
- **Within US3**: T016 and T017 can run in parallel; T018–T022 are sequential.
- **Within US5**: T026 and T027 can run in parallel; T028 depends on both.

---

## Parallel Example: User Story 1

```bash
# Add helper functions sequentially (same file ab/cli/parser.py):
Task: "T005 - _strip_rst() helper in ab/cli/parser.py"
Task: "T006 - _format_python_signature() helper in ab/cli/parser.py"
Task: "T007 - _format_cli_syntax() helper in ab/cli/parser.py"
Task: "T008 - _format_model_fields() helper in ab/cli/parser.py"

# Then sequentially:
Task: "T009 - Rewrite print_method_help() using above helpers"
Task: "T010 - Update __main__.py call site"
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002–T004)
3. Complete Phase 3: US1 — Rich CLI Help (T005–T010)
4. **STOP and VALIDATE**: Run `ab jobs get --help` and verify reference card
5. Commit checkpoint — MVP delivered

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 (Rich Help) → `--help` shows full reference cards → Commit
3. US2 (Auto-Discovery) → ExampleRunner entries simplified → Commit
4. US3 (Progress) → `progress.html` shows grouped view → Commit
5. US4 (Listings) → `ab jobs` shows enriched listing → Commit
6. US5 (Sphinx) → Docs aligned with CLI → Commit
7. US6 (Constants) → Generic discovery → Commit
8. Polish → Tests, lint, verification → Final commit

### Suggested MVP Scope

**US1 (Rich CLI Help)** alone delivers the highest value: every developer who runs `--help` immediately sees the improvement. Phases 1–3 (T001–T010) form a complete, shippable increment.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable at its checkpoint
- Commit after each phase completion
- All phases work on different files — no merge conflicts between parallel stories
- RouteResolver (T002) is the keystone — everything flows from it
