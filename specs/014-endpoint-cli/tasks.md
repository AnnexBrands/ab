# Tasks: Endpoint CLI

**Input**: Design documents from `/specs/014-endpoint-cli/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested. Existing test suite (232 passed) must remain green. CLI verification is manual smoke testing.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Create CLI package structure and register entry points

- [ ] T001 Create `ab/cli/__init__.py` with `main_prod()` and `main_staging()` functions that call `main(env=None)` and `main(env="staging")` respectively. Import `main` from `ab.cli.__main__`.

- [ ] T002 [P] Create `ab/cli/aliases.py` containing the `ALIASES` dict extracted from `examples/__main__.py`. This is the single source of truth for module aliases shared between `ex` and `ab`/`abs` CLIs. Include the full alias mapping: `addr→address`, `q→autoprice`, `cat→catalog`, `co→companies`, `ct→contacts`, `doc→documents`, `form→forms`, `job→jobs`, `lu→lookup`, `lot→lots`, `note→notes`, `parc→parcels`, `pay→payments`, `sell→sellers`, `ship→shipments`, `tk→timeline`, `track→tracking`, `u→users`, `lead→web2lead`.

- [ ] T003 [P] Update `examples/__main__.py` to import `ALIASES` from `ab.cli.aliases` instead of defining it locally. Remove the local `ALIASES` dict definition (lines 18-38). Add `from ab.cli.aliases import ALIASES` at the top of the file. Verify `ex --list` still works after this change.

- [ ] T004 Update `pyproject.toml` to add two new console-script entry points under `[project.scripts]`: `ab = "ab.cli:main_prod"` and `abs = "ab.cli:main_staging"`. Keep the existing `ex` entry.

- [ ] T005 Run `pip install -e .` to register the new entry points. Verify `ab` and `abs` commands are available (even if they don't do much yet).

**Checkpoint**: CLI package exists, aliases are shared, entry points registered. `ex --list` still works.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Endpoint discovery and method introspection — required by all user stories

- [ ] T006 Create `ab/cli/discovery.py` implementing endpoint discovery per the contract in `specs/014-endpoint-cli/contracts/cli-dispatcher.md`. Define `EndpointInfo` and `MethodInfo` as dataclasses or named tuples. Implement `discover_endpoints(api_or_cls)` that introspects `ABConnectAPI` to find all `BaseEndpoint` subclass attributes and enumerate their public methods. For each method, extract: name, `inspect.signature()`, docstring. Use class-level inspection (import endpoint classes from `ab.client` without instantiation) for `--list` operations that don't need credentials. Include `ParamInfo` extraction: separate positional params (path params) from keyword-only params (query params). Map `param_name` → `--param-name` CLI form (underscore→dash).

- [ ] T007 Create `ab/cli/formatter.py` implementing `format_result(result)` per the contract. Handle 5 result types: (1) Pydantic BaseModel → `model.model_dump(by_alias=True, mode="json")` then `json.dumps(indent=2)`, (2) list of BaseModel → serialize each, (3) dict/list → `json.dumps(indent=2)`, (4) primitive (str, int, bool, None) → `str(result)`, (5) bytes → `"<binary response, {len} bytes>"`. Import `BaseModel` from pydantic for type checking.

**Checkpoint**: Discovery and formatting modules ready. All downstream phases can use them.

---

## Phase 3: User Story 1 — Call an Endpoint from the CLI (Priority: P1)

**Goal**: `ab addr validate --line1=X --city=Y` calls the production API and prints JSON. `abs` does the same for staging.

**Independent Test**: Run `abs addr validate --line1="12742 E Caley Av" --city=Centennial --state=CO --zip=80111` and verify JSON output.

- [ ] T008 Create `ab/cli/parser.py` implementing `parse_cli_args(args, method_info)` per the contract. Parse `--param-name=value` and `--param-name value` (two-token) patterns. Map dashes to underscores (`--zip-code` → `zip_code`). Separate positional args (non-flag tokens before any `--` flag) from keyword args. Implement type coercion based on method signature annotations: `int` → `int(value)`, `bool` → `value.lower() in ("true", "1", "yes")`, `float` → `float(value)`, `dict`/`Any` → `json.loads(value)`. Handle `--body='{...}'` for JSON request bodies — parse JSON and pass as the `data` or `json` keyword argument. Return `(positional_args: list, keyword_args: dict)`.

- [ ] T009 Create `ab/cli/__main__.py` implementing the core dispatch logic per the contract. Implement `main(env=None)` that: (1) parses `sys.argv[1:]`, (2) handles `--list` at top level (list all endpoint groups with method counts and aliases — uses class-level discovery, no credentials needed), (3) resolves module name via exact/alias/prefix matching using `ALIASES` from `ab.cli.aliases`, (4) handles `module --list` (list all methods in that endpoint group with parameter signatures — no credentials needed), (5) for method invocation: creates `ABConnectAPI(env=env)`, introspects the endpoint instance, resolves method name via exact/prefix matching, parses remaining args via `parse_cli_args()`, calls the method, formats result via `format_result()`, prints to stdout. Support both dot syntax (`ab addr.validate`) and space syntax (`ab addr validate`) by splitting on `.` first. Print errors to stderr. Exit 0 on success, 1 on user error.

- [ ] T010 Verify US1 acceptance scenarios: (1) `abs addr validate --line1="12742 E Caley Av" --city=Centennial --state=CO --zip=80111` prints JSON, (2) `ab --list` shows all 23 endpoint groups with method counts, (3) `ab companies --list` shows all companies methods with signatures.

**Checkpoint**: Core CLI works end-to-end. Can list endpoints, list methods, and call methods with arguments.

---

## Phase 4: User Story 2 — Discover Methods and Parameters (Priority: P2)

**Goal**: `ab jobs --list` shows all methods with signatures. `ab addr validate --help` shows detailed parameter info.

**Independent Test**: Run `ab jobs --list` and verify all 31 methods shown with parameter names.

- [ ] T011 [US2] Enhance the `--list` output in `ab/cli/__main__.py` for module-level listing. For each method in an endpoint group, display: method name, positional params with types, keyword params with types and defaults. Use a tabular format similar to `ex`'s `_list_entries()`. Example output for address: `validate(*, line1: str, city: str, state: str, zip: str)`.

- [ ] T012 [US2] Add `--help` support to `ab/cli/parser.py` and wire it into `ab/cli/__main__.py`. When `--help` is in the args after a method is resolved, print the method's docstring (which contains `GET /address/isvalid`), full parameter listing with types and defaults, and example usage. Exit 0 after printing help.

**Checkpoint**: Discovery is self-documenting. Users can explore endpoints and methods without reading source code.

---

## Phase 5: User Story 3 — Parity with `ex` CLI (Priority: P2)

**Goal**: Same aliases, dot syntax, space syntax, and prefix matching as `ex`.

**Independent Test**: Run `ab co.get_by_id <uuid>` and `ab companies get_by_id <uuid>` and verify same result.

- [ ] T013 [US3] Implement prefix matching for method names in `ab/cli/__main__.py`. When a method name doesn't match exactly, find all methods starting with the given prefix. If exactly one match, use it. If multiple matches, print "Ambiguous method" with the matching names to stderr and exit 1. If no matches, print "Unknown method" with available methods and exit 1. This mirrors the behavior in `examples/__main__._resolve_entry()`.

- [ ] T014 [US3] Verify `ex` CLI parity: (1) `ab addr.validate --line1=X` (dot syntax) produces same result as `ab addr validate --line1=X` (space syntax), (2) `ab co` resolves to companies (alias), (3) `ab addr val` resolves to `validate` (prefix match), (4) `ab c` prints ambiguity message listing `catalog`, `commodities`, `commodity_maps`, `companies`, `contacts` (ambiguous prefix — same behavior as `ex c`), (5) `ab --list` and `ex --list` show same aliases.

**Checkpoint**: Full interaction parity with `ex`. Users familiar with `ex` can use `ab`/`abs` without learning new patterns.

---

## Phase 6: Error Handling + Edge Cases

**Purpose**: Graceful failures for auth, API errors, bad args, missing params

- [ ] T015 [P] Add authentication error handling in `ab/cli/__main__.py`. Wrap `ABConnectAPI(env=env)` creation in try/except to catch: (1) `FileNotFoundError` from missing `.env` or `.env.staging` file → print "Credentials not found. Create .env{.staging} with ABCONNECT_USERNAME, ABCONNECT_PASSWORD, ABCONNECT_CLIENT_ID, ABCONNECT_CLIENT_SECRET" to stderr, exit 2. (2) `ValidationError` from pydantic settings → print which field is missing, exit 2. (3) `requests.exceptions.ConnectionError` or auth failures → print HTTP status and message, exit 2.

- [ ] T016 [P] Add API error handling in `ab/cli/__main__.py`. Wrap the method invocation in try/except to catch: (1) `requests.exceptions.HTTPError` → print HTTP status code and response body to stderr, exit 2. (2) `requests.exceptions.ConnectionError` → print "Connection failed" to stderr, exit 2. (3) `requests.exceptions.Timeout` → print "Request timed out" to stderr, exit 2. (4) Generic `Exception` → print error message to stderr, exit 1.

- [ ] T017 [P] Add argument validation in `ab/cli/parser.py`. When unknown flags are passed (flags not matching any method parameter), print "Unknown argument: --flag-name" followed by "Valid parameters: ..." listing all accepted params, then exit 1. When required positional args are missing, print "Missing required argument: param_name" with the method signature, then exit 1.

**Checkpoint**: All edge cases from spec handled gracefully. No tracebacks shown to users.

---

## Phase 7: User Story 4 — Progress Review + Housekeeping (Priority: P3)

**Goal**: Verify and regenerate progress report. Confirm tests, ruff, and sphinx are green.

**Independent Test**: `python scripts/generate_progress.py` succeeds, `pytest` passes, `ruff check .` clean, `cd docs && make html` builds.

- [ ] T018 [US4] Run `python scripts/generate_progress.py` and verify it completes without errors. Check the summary output (endpoints, gate counts). If the generator itself has bugs (rendering, parsing), fix them. Do NOT attempt to fix individual endpoint gate failures (those are separate work).

- [ ] T019 [P] [US4] Run `pytest --tb=short -q` and verify 232+ passed, 0 failures. If any new failures appear from CLI changes (e.g., the `examples/__main__.py` alias import change from T003), fix them.

- [ ] T020 [P] [US4] Run `ruff check .` on the entire codebase including the new `ab/cli/` package. Fix any ruff violations found.

- [ ] T021 [P] [US4] Run `cd docs && make html` and verify it builds successfully. Warnings are acceptable, errors are not.

**Checkpoint**: All quality gates green. Progress report reflects current state.

---

## Phase 8: Polish + Final Verification

**Purpose**: End-to-end success criteria validation

- [ ] T022 Verify SC-001: Run `abs addr validate --line1="12742 E Caley Av" --city=Centennial --state=CO --zip=80111` and confirm valid JSON response.

- [ ] T023 Verify SC-002: Run `ab --list` and `ex --list` side by side. Confirm same endpoint group count (23) and same aliases.

- [ ] T024 Verify SC-005: Run `which ab && which abs` to confirm entry points are installed and functional.

- [ ] T025 Verify SC-006: Pick 3 example entries from different modules (e.g., `ex addr.validate`, `ex jobs.get`, `ex co.get_by_id`) and confirm the equivalent `ab`/`abs` commands work with the same alias and method name.

- [ ] T026 Regenerate `progress.html` one final time with `python scripts/generate_progress.py` and verify FIXTURES.md is current.

---

## Dependencies

```
T001 ──> T005 (entry points need __init__.py)
T002 ──> T003 (aliases must exist before examples import them)
T002 ──> T009 (aliases needed by dispatch)
T006 ──> T009 (discovery needed by dispatch)
T007 ──> T009 (formatter needed by dispatch)
T008 ──> T009 (parser needed by dispatch)

Phase 1 (T001-T005) ──> Phase 2 (T006-T007)
Phase 2 ──> Phase 3 (T008-T010) [US1 — core CLI]
Phase 3 ──> Phase 4 (T011-T012) [US2 — discovery UX]
Phase 3 ──> Phase 5 (T013-T014) [US3 — ex parity]
Phase 3 ──> Phase 6 (T015-T017) [error handling]
All ──> Phase 7 (T018-T021) [US4 — housekeeping]
All ──> Phase 8 (T022-T026) [final verification]
```

## Parallel Execution Opportunities

```
Phase 1: T002 || T003 (after T002 created, T003 can run; but T003 depends on T002)
Phase 2: T006 || T007 (independent files)
Phase 3: T008 creates parser.py, then T009 wires everything together
Phase 4: T011 || T012 (different files — __main__.py list vs parser.py help)
Phase 5: T013 (code) then T014 (verify)
Phase 6: T015 || T016 || T017 (different error domains, same files but independent sections)
Phase 7: T018 || T019 || T020 || T021 (all independent verification steps)
Phase 8: T022 || T023 || T024 || T025 (all independent verification)
```

## Implementation Strategy

**MVP (Phase 1-3)**: Setup + foundational + US1. After Phase 3, you have a working CLI that can list endpoints, list methods, and call any endpoint method with arguments. This alone delivers the core value proposition.

**Incremental from MVP**:
- Phase 4 (US2): Enhances discoverability — nice to have but not required for core functionality
- Phase 5 (US3): Ensures `ex` parity — important for adoption but the basic alias/prefix matching is already in US1
- Phase 6: Error handling — essential for production use but MVP works for happy path
- Phase 7-8: Housekeeping and verification — final polish

**Suggested approach**: Implement Phases 1-3 first, do a quick smoke test, then proceed through 4-8.
