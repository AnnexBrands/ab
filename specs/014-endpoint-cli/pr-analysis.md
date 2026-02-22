# PR Analysis: 014-endpoint-cli

**Branch**: `014-endpoint-cli`
**Date**: 2026-02-22
**Diff**: +1,869 / -21 across 18 files (6 implementation, 2 config, 2 docs, 8 spec)

---

## Code Quality Assessment

### Grade: B+

Solid implementation that delivers all core user stories with clean module decomposition. A few bugs in edge-case paths need attention before production use.

### Module Decomposition

The five-module split (`__init__`, `__main__`, `aliases`, `discovery`, `parser`, `formatter`) follows single-responsibility well. Each has a clear role and the dependency graph is acyclic. The alias-sharing pattern between `ex` and `ab`/`abs` via a single source of truth in `aliases.py` is a smart design choice that eliminates drift.

### Bugs Found

**1. `--body` dispatch makes double API calls** (`__main__.py:246-250`)

When `body is not None` and the first call returns `None`, the code fires a *second* live API call with `data=body`. This is a real side-effect bug — `None` can be a valid return value. The branching on `if keyword` to decide between `json=body` and positional is also fragile.

**2. `--body` two-token form skips next argument** (`parser.py:109-111`)

In `--body '{"k":1}' --other=val`, the `i += 1` inside the `--body` handler combined with the `i += 1` consumed by the two-token parse at line 100 causes a double-increment, skipping `--other=val`.

**3. `exc.response` can be `None`** (`__main__.py:255`)

`requests.ConnectionError` has a `response` attribute that is `None`. The `hasattr(exc, "response")` check passes, then `exc.response.status_code` raises `AttributeError`.

### Dead Code

- `discover_endpoints_from_instance()` in `discovery.py:165-213` — 50 lines, never called. Was presumably the original plan before class-level discovery proved sufficient. Should be removed or deferred to a future feature.
- `MethodInfo.callable` field — only set by the dead code path above. Misleading in the dataclass.

### Code Smells

- `import re` inside function body (`discovery.py:142`) — should be at module top.
- Redundant branching at `__main__.py:201-213` — both paths call `_list_methods` and return.
- No `try/except` around `json.loads` for `--body` parsing (`parser.py:110`) — uncaught `JSONDecodeError` produces a traceback instead of a user-friendly message.

---

## Spec Coherence

### Requirements Coverage

| Requirement | Status | Notes |
|---|---|---|
| FR-001: Console-script entry points | PASS | `ab` and `abs` registered in pyproject.toml |
| FR-002: Shared aliases | PASS | Single source of truth in `aliases.py` |
| FR-003: Three dispatch syntaxes | PASS | Dot, space, bare module all work |
| FR-004: Prefix matching + ambiguity | PASS | Matches `ex` behavior exactly |
| FR-005: CLI args as kwargs | PASS* | `--body` has the skip bug noted above |
| FR-006: Dynamic introspection | PASS | Regex-based source inspection — fragile but functional |
| FR-007: JSON output | PASS | All 5 result types handled |
| FR-008: Exit codes | PASS | 0/1/2 consistently applied |
| FR-009: --list at top/module level | PASS | Both levels work without credentials |
| FR-010: Progress report | PASS | Generated successfully (24/161 gates) |

### User Story Coverage

- **US1** (Call endpoints): Fully implemented and working.
- **US2** (Discovery): `--list` and `--help` both functional.
- **US3** (Parity with `ex`): Aliases, prefix matching, dot/space syntax all verified.
- **US4** (Housekeeping): Progress report regenerated, tests passing (232/0/73), ruff clean on feature files.

### Gaps

- Spec mentions stdin support for `--body` in Assumptions section — not implemented.
- Three phantom aliases (`parc→parcels`, `tk→timeline`, `track→tracking`) reference endpoints that don't exist on `ABConnectAPI`. Inherited from `ex` but should be cleaned up.

---

## Architecture Review

### Discovery Approach

The regex-based source inspection of `_init_endpoints` (`discovery.py:140-144`) is the most architecturally fragile component. It avoids needing credentials for `--list` (good), but any refactoring of `_init_endpoints` formatting will break discovery silently. No test validates the expected endpoint count.

A more robust future approach: a class-level registry on `ABConnectAPI` or `__init_subclass__` hooks on `BaseEndpoint`. The current approach is acceptable for an initial implementation since it avoids modifying existing SDK code.

### Parser Design

Custom argument parser handles the common cases well. Type coercion from `inspect.signature` annotations is clever. The `POSITIONAL_OR_KEYWORD` classification forces users to know positional argument order for methods like `jobs.update_timeline_task(job_display_id, task_id, data)` — worth documenting.

### Security

No concerns. Arguments flow as Python function parameters, no shell execution. Credentials are loaded by the SDK, never printed. `json.loads` for `--body` is safe.

---

## Constitution & Plan Coherence

The spec, plan, research, data-model, contracts, and tasks are thorough and internally consistent. The 8-phase plan decomposition is well-structured and the dependency graph is clear. Research decisions (class-level vs instance-level discovery, custom parser vs argparse) are documented with rationale.

The tasks.md is granular enough for independent implementation of each phase, with clear checkpoint criteria. The parallel execution opportunities are correctly identified.

One structural improvement: the plan could benefit from a "known limitations" section that explicitly scopes out stdin support and test coverage.

---

## Progress Toward Project Goals

This feature completes a significant DX milestone: developers can now call any of the 226 API methods across 23 endpoint groups from the terminal without writing Python scripts. Combined with the `ex` example runner, the SDK now provides both "see how it works" (`ex`) and "just call it" (`ab`/`abs`) CLI workflows.

### SDK Maturity Scorecard

| Area | Status |
|---|---|
| Core SDK (endpoints, models, auth) | Stable — 23 endpoints, 226 methods |
| Test coverage | 232 passing, 73 skipped (live tests) |
| Quality gates | 24/161 endpoints pass all gates |
| CLI tooling | Complete — `ex` (examples) + `ab`/`abs` (live calls) |
| Documentation | Sphinx builds, FIXTURES.md tracking in place |

---

## Recommended Next Steps

### Immediate (before merge)

1. Fix the `--body` double-dispatch bug (`__main__.py:246-250`)
2. Fix the `--body` two-token parser skip bug (`parser.py:111`)
3. Guard `exc.response is None` in error handler (`__main__.py:255`)

### Next Feature Cycle

1. **Add CLI unit tests** — `parse_cli_args`, `_coerce_value`, `discover_endpoints_from_class`, `format_result`. Even 10-15 tests would catch the bugs found in this review.
2. **Remove dead code** — `discover_endpoints_from_instance()` and `MethodInfo.callable`.
3. **Clean phantom aliases** — remove `parc`, `tk`, `track` from `aliases.py` (or add the missing endpoints).
4. **Quality gate push** — 24/161 is low. Focus on fixture coverage for the highest-traffic endpoints.
5. **Consider replacing regex discovery** with a registry pattern on `ABConnectAPI` that's resilient to refactoring.
