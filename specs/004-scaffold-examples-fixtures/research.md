# Research: Scaffold Examples & Fixtures

**Feature**: 004-scaffold-examples-fixtures
**Date**: 2026-02-14

## Decision 1: Runner Pattern — Class-Based with Entry Registration

**Decision**: Implement a runner as a Python class in `examples/_runner.py` that manages structured entry registration, selective execution via CLI args, and automated fixture capture.

**Rationale**: ABConnectTools uses an `ExampleRunner` base class with `add(name, description, func)` registration and CLI-driven execution (`sys.argv` parsing). This pattern cleanly separates entry metadata from execution logic, supports selective runs (e.g., `python -m examples.address validate`), and provides a natural place for fixture-save logic. The AB SDK currently has no runner — examples are flat scripts with manual `ABConnectAPI()` initialization and direct method calls.

**Alternatives Considered**:
- **Decorator-based** (`@example(name="validate", ...)`): Cleaner syntax per entry, but harder to control execution order and CLI selection. Requires module-level registration which complicates selective imports.
- **YAML/JSON manifest**: Metadata in a separate file, code in Python. Introduces a sync problem between manifest and code — violates the "single source of truth" principle.
- **Flat scripts (status quo)**: No runner, no structured entries. Does not support automated fixture capture or surface-area inventory.

## Decision 2: Fixture Capture Flow — Model Round-Trip

**Decision**: The runner captures fixtures by: (1) calling the endpoint method (which already casts responses to Pydantic models via `_request()`), (2) serializing the model back to a camelCase dict via `model_dump(by_alias=True, mode="json")`, (3) writing JSON to `tests/fixtures/{ModelClassName}.json`.

**Rationale**: The `BaseEndpoint._request()` method already resolves `Route.response_model` and calls `model_validate()` on responses. The returned object is a validated Pydantic model. Serializing back via `model_dump(by_alias=True)` preserves camelCase keys and handles special types (datetime→ISO, UUID→string). `ResponseModel` uses `extra="allow"`, so unknown API fields are preserved through the round-trip. This matches the user's stated flow: "cast to the model, then to json, then call save fixture."

**Alternatives Considered**:
- **Capture raw JSON before model parsing**: Would require modifying `_request()` or `HttpClient` to return both raw and parsed. More invasive, and raw JSON may have inconsistent formatting.
- **Use `response.json()` directly**: Bypasses model validation entirely — fixtures would not be guaranteed to parse against the model, defeating the validation purpose.

## Decision 3: Entry Metadata — Declared Per Method

**Decision**: Each structured entry declares: method name, callable (the API call), response model name, request model name (if any), and fixture file name. These are passed as arguments to `runner.add()`.

**Rationale**: The Route dataclass already holds `request_model` and `response_model` as string names, but Route objects are module-private constants in endpoint files (e.g., `_IS_VALID`). Rather than exposing Route internals, entries redeclare the metadata explicitly. This keeps examples self-documenting — a developer can read the entry and see all metadata without navigating to endpoint source code. ABConnectTools follows the same pattern: metadata is at the call site, not hidden in infrastructure.

**Alternatives Considered**:
- **Introspect Route from endpoint method**: Would require endpoint methods to expose their Route or adding a public registry. Cleaner DRY but couples examples to internal implementation details.
- **Generate entries from Route definitions**: Auto-generation eliminates manual sync but produces boilerplate without real request parameters — still needs manual TODO filling.

## Decision 4: Package Structure — `examples/` as a Python Package

**Decision**: Convert `examples/` to a Python package by adding `__init__.py`. This enables `python -m examples.address` execution and allows shared imports from `examples/_runner.py`.

**Rationale**: The user's description specifies `python -m examples.address` as the execution pattern. This requires `examples/` to be a package. The `_runner.py` module uses a leading underscore to signal it's infrastructure, not a user-facing example.

**Alternatives Considered**:
- **Keep as loose scripts**: Current state. Cannot use `python -m` execution, cannot share runner import.
- **Separate `tools/` directory for runner**: Splits infrastructure from examples, complicating imports and discoverability.

## Decision 5: Existing Example Migration Strategy

**Decision**: Migrate all 16 existing example files to the runner pattern in place. Preserve all existing method calls by wrapping them as `runner.add()` entries with the correct metadata. No functionality loss.

**Rationale**: Migrating in place (rather than creating new files alongside old ones) avoids confusion and file bloat. The existing examples already demonstrate the correct API calls — they just need wrapping in the runner structure and metadata annotation. The 22 already-captured fixtures have known request parameters that should be populated in their entries. The 27 pending fixtures get TODO annotations.

**Alternatives Considered**:
- **Create new files, deprecate old**: Two files per module during transition. Confusing for developers and violates "no file bloat" principle.
- **Gradual migration**: Migrate one at a time over multiple PRs. Increases merge complexity and leaves inconsistent patterns in the codebase.

## Decision 6: TODO Convention for Incomplete Entries

**Decision**: Use `# TODO: capture fixture — <specific reason from FIXTURES.md>` for entries whose request data is incomplete. The runner detects TODO markers in callable source or uses a sentinel parameter value to skip execution of incomplete entries.

**Rationale**: FIXTURES.md already documents what each pending endpoint needs (e.g., "needs valid street, city, state, zipCode"). Embedding this in the example as a TODO comment makes the gap visible at the point of action. ABConnectTools does not have this pattern — all its examples use live data. For the AB SDK, where 27 endpoints are pending, TODOs bridge the gap between "example exists" and "example captures fixture."

**Alternatives Considered**:
- **Separate "pending" list file**: Duplicates FIXTURES.md information. Out of sight, out of mind.
- **Disabled flag per entry**: `runner.add(..., enabled=False)` — machine-readable but doesn't convey what's missing or why.

## Reference: ABConnectTools Patterns Observed

The following patterns from ABConnectTools informed these decisions (clean-room — no code copied):

1. **ExampleRunner base class** with `add(name, desc, func)` registration — confirmed the class-based runner approach.
2. **`save_fixture(obj, name)` helper** — uses `model_dump(by_alias=True)` for Pydantic, `json.dumps` for dicts. Idempotent (skips if file exists). Informed fixture save design.
3. **`_constants.py`** with centralized test IDs (job IDs, company UUIDs) — AB SDK uses `tests/constants.py` for similar purpose.
4. **CLI execution** via `sys.argv` parsing in runner — confirmed selective entry execution pattern.
5. **Lazy API client** via `@property` — avoids initialization cost when just listing examples.
