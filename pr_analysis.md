# PR Analysis: CLI Docs & Discovery Major Release

**Branch**: `025-cli-docs-discovery`
**Base**: `main`
**Date**: 2026-03-01
**Scope**: 15 files changed, +969/-333 lines, 6 user stories, 37 tasks across 9 phases
**Reviewers**: CTO, Head of Engineering, Lead Engineer

---

## Executive Summary

This PR makes the `Route` dataclass the single source of truth for CLI help, auto-discovery, progress reporting, and test-constant generation. It delivers six user stories: rich `--help` reference cards, ExampleRunner model auto-population, grouped progress tracking, enriched method/endpoint listings, Sphinx docstring alignment, and generic constants discovery.

The architectural direction is correct. The `Route`-as-backbone pattern is the right long-term choice for this SDK. The CLI help cards are genuinely useful and the auto-discovery eliminates a real class of copy-paste drift. However, three independent reviewers identified two concrete bugs and several design limitations that require attention.

**Verdict: MERGE WITH CHANGES** — Fix the two blockers (body dispatch crash, regex false positive), then merge. Schedule follow-up for FormsEndpoint coverage and auto-discovery tests.

---

## What Ships

### US1: Rich CLI Help (P1)

`ab jobs get --help` now prints a structured reference card:

```
  get
  ───

  GET /job/{jobDisplayId} (ACPortal)

  Route   GET /job/{jobDisplayId}
  Python  api.jobs.get(job_display_id: int) -> Job
  CLI     ab jobs get <job_display_id>

  Returns: Job

  Positional arguments:
    job_display_id (int)

  Response model: Job
    is_active            bool | None    Whether the record is active
    created_date         datetime | None Creation timestamp
    job_display_id       int | None     Human-readable job ID
    status               str | None     Job status
    ... (29 more fields)
```

No credentials required. Purely introspective — reads source code and model metadata at startup time.

### US2: Route-Derived Auto-Discovery (P1)

ExampleRunner entries no longer need explicit `response_model` or `fixture_file`:

```python
# Before — explicit, error-prone, drifts from Route definition:
runner.add("get", lambda api: api.jobs.get(12345),
           response_model="Job", fixture_file="Job.json")

# After — auto-populated from Route metadata:
runner.add("get", lambda api: api.jobs.get(12345))
# response_model="Job" and fixture_file="Job.json" inferred automatically
```

Explicit values still override. Three entries in `examples/jobs.py` simplified as proof of concept.

### US3: Upgraded Progress Tracking (P1)

`progress.html` groups endpoints by class with sub-sections by path sub-root (e.g., jobs → timeline, onhold, parcelitems). Each row shows Python dotted path (`api.jobs.get_timeline`), example status, and CLI status. FIXTURES.md includes a new "Python Path" column.

### US4: Method Listing (P2)

`ab jobs` implicitly lists all 57 methods showing HTTP verb, path, params, and return type. Helpers (no Route) appear in a separate section:

```
  jobs — 57 methods

  Helpers (no API route):
  ──────────────────────────────────────────────────
  get_timeline                   job_display_id
  get_timeline_agent             job_display_id, task_code

  API Methods:
  ────────────────────────────────────────────────────────
  GET  /job/{jobDisplayId}           get(job_display_id) -> Job
  POST /job/{jobDisplayId}/timeline  create_timeline_task(...) -> TimelineSaveResponse
  ...
```

`ab` alone shows endpoint groups with path roots and aliases:

```
  Endpoint             Methods   Path Root         Aliases
  ──────────────────── ───────   ───────────────   ──────────────
  address                    2   /address          addr
  companies                 26   /companies        co
  contacts                  12   /contacts         ct
  jobs                      57   /job              job
  ...
  23 endpoints, 237 methods
```

### US5: Sphinx Docstrings (P2)

Three representative docstrings in `jobs.py` updated with Args/Returns sections and `:class:` cross-references. Establishes the convention for future docstring passes.

### US6: Generic Constants Discovery (P2)

Replaced hardcoded `_PARAM_CONSTANT_MAP` with generic `path_param_to_constant()` converting any camelCase path param to `TEST_SCREAMING_SNAKE` format.

---

## Architecture

### Core Pattern: RouteResolver

The keystone of this feature is `ab/cli/route_resolver.py` — a 63-line module that maps endpoint methods to `Route` constants via source-code introspection:

```python
_ROUTE_REF_RE = re.compile(r"(?:self\._request|_request)\(\s*(_[A-Z_][A-Z0-9_]*)")
```

For each public method on an endpoint class, it reads the source via `inspect.getsource()`, regex-matches the Route constant name passed to `self._request()`, and returns a `{method_name: Route}` mapping.

**Why source introspection?** Endpoint classes require authentication to instantiate. The CLI help and progress systems must work without credentials. Source-code analysis avoids instantiation entirely.

**Hit rate**: 210/237 methods resolved (88.6%) across 23 endpoint classes. The 27 unresolved methods fall into documented categories:
- Wrapper methods delegating to other public methods (e.g., `get_timeline` → `get_timeline_response`)
- Methods using `self._client.request()` directly (e.g., `get_timeline_agent`, `documents.upload`)
- Methods routing through helper functions (e.g., FormsEndpoint's `_pdf()` pattern)

**Multiline call handling**: The `\s*` in the regex matches newlines by default in Python, so multiline calls like `self._request(\n    _TRANSFER.bind(...)` are correctly matched. Verified against 36+ multiline calls in `jobs.py`.

### Data Flow

```
Route (frozen dataclass — single source of truth)
  ↓
RouteResolver (inspect.getsource + regex)
  ↓
MethodInfo.route / EndpointInfo.path_root / EndpointInfo.aliases
  ↓
┌─────────────────┬──────────────────┬─────────────────────┬───────────────┐
│ CLI --help       │ ExampleRunner    │ progress.html       │ FIXTURES.md   │
│ (parser.py)      │ (_runner.py)     │ (renderer.py)       │ (fixtures_gen)│
└─────────────────┴──────────────────┴─────────────────────┴───────────────┘
```

### Dependencies

- **No new external dependencies** — uses stdlib (`inspect`, `re`, `pkgutil`, `importlib`) and existing pydantic
- **Internal coupling**: `ab.progress` → `ab.cli.discovery` → `ab.cli.route_resolver` (one-directional; no circular dependency; both progress imports are lazy/inside function bodies)
- **stderr convention**: All help and listing output goes to stderr; API results go to stdout. This is the correct Unix pattern — `ab jobs get 12345 | jq .` works because only JSON hits stdout.

---

## Files Changed

### New Files (3)

| File | Lines | Purpose |
|------|-------|---------|
| `ab/cli/route_resolver.py` | 63 | RouteResolver: method→Route mapping via source introspection; `path_param_to_constant()` |
| `tests/unit/test_route_resolver.py` | 60 | 10 tests: 4 for route resolution, 6 parametrized for constant conversion |
| `tests/unit/test_cli_output.py` | 138 | 15 tests: RST stripping, signature formatting, CLI syntax, help output, discovery |

### Modified Files (12)

| File | +/- | Changes |
|------|-----|---------|
| `ab/cli/discovery.py` | +76 | Extended `MethodInfo` (route, return_annotation), `EndpointInfo` (aliases, path_root); route resolution in `discover_endpoints_from_class()` |
| `ab/cli/parser.py` | +194 | Helper functions (`_strip_rst`, `_format_python_signature`, `_format_cli_syntax`, `_format_model_fields`); rewrote `print_method_help()` |
| `ab/cli/__main__.py` | +87/-40 | Rewrote `_list_methods()`, `_list_all()`; simplified dispatch; pass `module_name` to help |
| `examples/_runner.py` | +103 | `endpoint_attr`, `_resolve_method_routes()`, `_auto_populate_entry()` for auto-discovery |
| `examples/jobs.py` | +11/-6 | Added `endpoint_attr="jobs"`; removed explicit models from 3 entries |
| `ab/progress/models.py` | +36 | `MethodProgress` and `EndpointClassProgress` dataclasses |
| `ab/progress/route_index.py` | +139 | `build_endpoint_class_progress()`, `_extract_sub_root()`, `_scan_example_entries()` |
| `ab/progress/renderer.py` | +91 | `render_endpoint_class_progress()`, `_yn_badge()`; updated `render_report()` signature |
| `ab/progress/fixtures_generator.py` | +27 | "Python Path" column in FIXTURES.md |
| `ab/progress/instructions.py` | +25/-23 | Generic `path_param_to_constant()` replaces hardcoded `_PARAM_CONSTANT_MAP` |
| `scripts/generate_progress.py` | +6 | Wires `build_endpoint_class_progress()` into report generation |
| `ab/api/endpoints/jobs.py` | +33/-15 | Updated 3 docstrings with Args/Returns/`:class:` cross-references |

---

## Test Results

```
512 passed, 25 new, 9 pre-existing failures, 65 skipped, 5 xfailed (6.04s)
```

**25 new tests** across 2 files:
- `test_route_resolver.py`: Route resolution against live endpoint classes, `path_param_to_constant` parametrized cases
- `test_cli_output.py`: RST stripping, Python signature formatting, CLI syntax formatting, help output assertions, discovery integration (aliases, path_root, method routes, return annotations)

**9 pre-existing failures** (all unrelated to this PR):
- `test_parcel_models` / `test_tracking_models` / `test_user_models`: Missing fixture JSON files
- `test_mock_coverage`: Fixture tracking out of sync
- `test_jobs_search`: Pydantic validation error (model/API mismatch predating this branch)

---

## Council Review

### CTO — Strategic Alignment & Risk

| Criterion | Grade | Assessment |
|---|---|---|
| Strategic Alignment | **B+** | Route-as-truth is the right direction. Scope mostly justified — US5 (3/237 docstrings) feels thin as a "user story" |
| Architectural Integrity | **B-** | RouteResolver concept is sound; regex implementation has a 12% miss rate with a catastrophic failure on FormsEndpoint (5% resolution) |
| Risk Assessment | **C+** | US6 constants regression (`companyId` → `TEST_COMPANY_ID` but actual constant is `TEST_COMPANY_UUID`); `inspect.getsource()` deployment constraint undocumented |
| Technical Debt | **B** | Net neutral — auto-discovery reduces drift but regex introspection creates a new maintenance trap |
| Missing Pieces | **C** | Zero tests for `_auto_populate_entry`, `build_endpoint_class_progress`, `_scan_example_entries`; `has_cli` column always True (meaningless) |
| Production Readiness | **C+** | Fix constants regression, add auto-discovery tests, document FormsEndpoint gap |

**CTO verdict**: "The vision is right. Route-as-truth direction is correct. But the regex miss rate, constants regression, and test coverage gaps need another iteration."

---

### Head of Engineering — Code Quality & Bugs

| Criterion | Grade | Assessment |
|---|---|---|
| Code Quality | **C+** | Clean structure, good dataclasses, but actual bugs confirmed |
| Test Coverage | **D+** | 25 tests cover happy path only; zero tests for the bugs found; no edge cases |
| Architecture | **C** | RouteResolver is a single point of failure with confirmed false positives AND false negatives |
| Process/Risk | **C-** | 37 tasks in one PR; 9 pre-existing failures tolerated; only 3 docstrings updated |
| Production Readiness | **D+** | `--body` dispatch will crash at runtime; resolver has confirmed false positive |

#### Critical Finding 1: `--body` CLI Dispatch is Broken

In `__main__.py:264-269`, the body-handling code path has **never been tested** and will crash on first use:

```python
if body is not None:
    result = live_method(*positional, json=body) if keyword else live_method(*positional, body)
    if result is None:
        result = live_method(*positional, data=body, **keyword)
```

**Problem A**: `live_method(*positional, body)` passes body as a positional arg, but endpoint methods use `data=` keyword-only params. **TypeError at runtime.**

**Problem B**: `json=body` keyword doesn't match endpoint method signatures (they use `data=`, not `json=`). **TypeError at runtime.**

**Problem C**: Retry-on-None logic could **double-execute destructive operations** (POST, DELETE) if the first call legitimately returns None.

#### Critical Finding 2: Regex False Positive on `_paginated_request`

The regex `_request\(` matches as a substring inside `self._paginated_request(_LIST, ...)`. Confirmed:

```python
>>> source = "self._paginated_request(\n            _LIST, ..."
>>> _ROUTE_REF_RE.search(source)
<re.Match ... match='_request(\n            _LIST'>
```

Currently produces correct results **by coincidence** (route constant IS the first argument to `_paginated_request`), but the match mechanism is wrong. A new `_custom_request()` helper would produce genuine false positives.

#### Critical Finding 3: FormsEndpoint 95% Miss Rate

19 of 20 methods in FormsEndpoint route through `self._pdf(_ROUTE, ...)` instead of `self._request()`. The CLI shows them as "Helpers (no API route)" when they are all API methods. **User-visible incorrect information.**

**Head of Engineering verdict**: "Do not merge as-is. Fix the `--body` crash (mandatory), fix the regex word boundary (mandatory), add tests for resolver limitations (strongly recommended)."

---

### Lead Engineer — Craftsmanship & Edge Cases

**Overall craftsmanship**: 7/10

#### Validations (things that work correctly)

| Concern | Status | Analysis |
|---|---|---|
| Multiline regex matching | **Correct** | `\s*` matches `\n` by default in Python; verified against 36+ multiline calls |
| `_format_model_fields` generic handling | **Adequate** | `List[X]` regex sufficient — no nested generics exist in any Route's `response_model` |
| `path_param_to_constant` edge cases | **Not applicable** | `HTMLParser`/`companyID` patterns don't exist in this codebase; all params are clean camelCase |
| stderr output pattern | **Correct** | Unix convention; API results → stdout, help/listings → stderr; pipes work correctly |
| Circular dependency risk | **None** | Import graph is one-directional: progress → CLI → route_resolver |
| `_field_type_str` Union handling | **Correct** | `type(int | str) is types.UnionType` works on Python 3.14 |

#### Confirmed Bugs

| Bug | Severity | Location |
|---|---|---|
| `--body` dispatch crash | **HIGH** | `__main__.py:264-269` |
| `get_timeline_agent` silently missed | **MEDIUM** | Uses `self._client.request()` not `self._request()` |
| `_coerce_value("-")` IndexError | **TRIVIAL** | `parser.py:133-162` — `value[1:]` on single char `"-"` |

#### Minor Issues

- `_compute_path_root` has an unnecessarily complex code path for the multi-root case
- `_scan_example_entries` broad `except Exception: continue` swallows SyntaxError/ImportError
- No `logger.debug()` in `inspect.getsource()` except block — silent failures invisible during development

**Lead Engineer verdict**: "MERGE WITH CHANGES. Fix the `--body` handling (mandatory), add documentation comments for known regex limitations (recommended). The architecture is sound — source introspection to avoid instantiation is the right call for a credentials-free CLI."

---

## Consolidated Risk Matrix

### Must Fix (Blockers)

| # | Issue | Severity | Location | Fix |
|---|-------|----------|----------|-----|
| 1 | `--body` dispatch crash: passes body as positional arg, wrong keyword, retry-on-None | **HIGH** | `__main__.py:264-269` | Replace with `result = live_method(*positional, data=body, **keyword)` |
| 2 | Regex false positive on `_paginated_request` | **MEDIUM** | `route_resolver.py:15` | Add word boundary: `r"(?:self\.|\b)_request\("` or anchor match |

### Should Fix (Strongly Recommended)

| # | Issue | Severity | Location | Fix |
|---|-------|----------|----------|-----|
| 3 | Document known resolver limitations | **MEDIUM** | `route_resolver.py` | Add module-level docstring listing known miss patterns |
| 4 | Extend regex to catch `self._pdf(_ROUTE` for FormsEndpoint | **MEDIUM** | `route_resolver.py:15` | Add `_pdf` to alternation: `(?:self\._request\|self\._pdf\|_request)` |
| 5 | Add tests for ExampleRunner auto-discovery | **MEDIUM** | New test file | Test auto-population, `List[X]` handling, explicit override precedence |

### Consider (Nice to Have)

| # | Issue | Severity | Location | Fix |
|---|-------|----------|----------|-----|
| 6 | Add `logger.debug()` in getsource except block | **LOW** | `route_resolver.py:41` | Visibility during development |
| 7 | Cache `discover_endpoints_from_class()` with `@lru_cache` | **LOW** | `discovery.py` | Avoid redundant introspection |
| 8 | Add override map for `companyId` → `TEST_COMPANY_UUID` | **LOW** | `instructions.py` | Restore context-specific constant names |
| 9 | Make `has_cli` conditional or remove from progress display | **LOW** | `route_index.py` | Eliminate meaningless always-True column |
| 10 | Narrow `except Exception` in `_scan_example_entries` | **LOW** | `route_index.py:200` | Catch only `ImportError`, `AttributeError` |

---

## Specification Traceability

| User Story | Status | Acceptance | Evidence |
|---|---|---|---|
| US1: Rich CLI Help | **Complete** | All criteria met | 7/7 quickstart scenarios pass; Route, Python sig, CLI syntax, model fields shown |
| US2: Auto-Discovery | **Complete** | All criteria met | `response_model` and `fixture_file` auto-populated; explicit overrides preserved |
| US3: Progress Tracking | **Complete** | All criteria met | Grouped by class and sub-root; dotted paths; ex/cli columns; FIXTURES.md Python Path |
| US4: Method Listing | **Complete** | All criteria met | HTTP verbs, paths, return types; helpers separated; aliases and path roots |
| US5: Sphinx Docstrings | **Partial** | Convention established | 3/237 methods updated — establishes pattern, does not complete sweep |
| US6: Generic Constants | **Complete with caveat** | Converter works | `companyId`/`id` produce different constants than old hardcoded map |

---

## Design Artifacts

The feature was developed through the full speckit workflow:

| Artifact | Path | Purpose |
|---|---|---|
| Specification | `specs/025-cli-docs-discovery/spec.md` | 6 user stories, 3 clarifications resolved |
| Implementation Plan | `specs/025-cli-docs-discovery/plan.md` | Tech stack, architecture, phases |
| Task Breakdown | `specs/025-cli-docs-discovery/tasks.md` | 37 tasks across 9 phases (all complete) |
| Technical Research | `specs/025-cli-docs-discovery/research.md` | Route introspection approaches evaluated |
| Data Model | `specs/025-cli-docs-discovery/data-model.md` | MethodProgress, EndpointClassProgress |
| Smoke Tests | `specs/025-cli-docs-discovery/quickstart.md` | 7 verification scenarios (all passing) |
| CLI Contract | `specs/025-cli-docs-discovery/contracts/cli-help-format.md` | Help output format specification |
| Quality Checklist | `specs/025-cli-docs-discovery/checklists/requirements.md` | All items pass |

---

## Test Coverage Assessment

| Component | Tests | Gaps |
|---|---|---|
| Route resolution (RouteResolver) | 4 tests against live endpoints | Missing: false positive case, false negative documentation, error paths |
| Constant conversion | 6 parametrized cases | Adequate for actual parameter patterns |
| RST stripping | 3 tests | Adequate |
| Python signature formatting | 2 tests | Adequate |
| CLI syntax formatting | 2 tests | Adequate |
| Help output content | 3 tests (route line, python sig, CLI syntax) | Missing: model fields section, request/params model sections |
| Discovery integration | 5 tests (registry, aliases, path_root, route, return_annotation) | Adequate |
| ExampleRunner auto-discovery | **0 tests** | Missing: `_auto_populate_entry`, `List[X]` parsing, explicit override |
| Progress report grouping | **0 tests** | Missing: `build_endpoint_class_progress`, `_scan_example_entries` |
| Progress HTML rendering | **0 tests** | Missing: `render_endpoint_class_progress` |
| `--body` CLI dispatch | **0 tests** | **Bug confirmed** — will crash on first use |

---

## Conclusion

The architectural direction is sound — `Route` as the single source of truth for metadata is the right long-term investment for this SDK. The CLI help cards are immediately useful. The auto-discovery eliminates a real class of copy-paste errors. The progress grouping gives meaningful visibility into SDK coverage. The implementation is competent, with clean separation across discovery, parsing, formatting, and rendering.

The PR has two concrete bugs that must be fixed before merge:
1. **The `--body` dispatch will crash at runtime** — a straightforward fix to use `data=body` keyword
2. **The regex false positive on `_paginated_request`** — a word-boundary fix

The RouteResolver's 12% miss rate and the FormsEndpoint gap are acknowledged design limitations of the source-introspection approach. They should be documented and the regex extended to cover `_pdf()` delegation. Test coverage of new features beyond the CLI formatter functions should be improved in a fast-follow.

**Recommendation**: Fix the two blockers, merge, and schedule follow-up work for FormsEndpoint regex extension, ExampleRunner auto-discovery tests, and the constants override map.

---

*Analysis performed 2026-03-01 by council of: CTO, Head of Engineering, Lead Engineer.*
*Research validated against live codebase execution, regex pattern analysis, and endpoint source inspection.*
