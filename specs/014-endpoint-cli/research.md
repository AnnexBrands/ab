# Research: Endpoint CLI

**Feature**: 014-endpoint-cli
**Date**: 2026-02-22

## Decision 1: CLI Entry Point Architecture

**Decision**: Two separate console-script entry points (`ab` and `abs`) that both call the same `main()` function with different defaults, rather than a single entry point with an `--env` flag.

**Rationale**: The user explicitly requested `ab` for production and `abs` for staging. Two entry points are simpler to type and remember. The environment is the only difference — both share identical dispatch logic. Implementation: `ab` calls `main(env=None)` (production default), `abs` calls `main(env="staging")`.

**Alternatives considered**:
- **Single entry point with `--env` flag** (`ab --env staging addr validate`) — Rejected: adds boilerplate to every staging call. The user wants `abs` as a shortcut.
- **Environment variable** (`AB_ENV=staging ab addr validate`) — Rejected: inconvenient, easy to forget, not what was requested.

## Decision 2: Endpoint Discovery Strategy

**Decision**: Introspect the `ABConnectAPI` instance at runtime by iterating its attributes and identifying `BaseEndpoint` subclass instances. For each endpoint, enumerate public methods (excluding `_`-prefixed) via `inspect.getmembers()`.

**Rationale**: The `ABConnectAPI` constructor eagerly instantiates all 23 endpoint attributes. We can inspect them without calling any API. Method signatures (via `inspect.signature()`) give us parameter names, types, and defaults — everything needed for CLI argument parsing.

**Alternatives considered**:
- **Static registry** (manually maintained list of endpoint→methods) — Rejected: maintenance burden, falls out of sync when endpoints are added.
- **Import-time scanning of endpoint modules** — Rejected: misses the client's attribute naming (e.g., `self.rfq` for `RFQEndpoint`). The client is the source of truth for attribute names.

## Decision 3: Argument Parsing Strategy

**Decision**: Parse `--param-name=value` and `--param-name value` patterns from CLI arguments. Map `param-name` to Python `param_name` (dash→underscore). No dependency on argparse or click — use a lightweight custom parser that mirrors the endpoint method's `inspect.signature()`.

**Rationale**: Endpoint methods use keyword-only arguments with Python naming (`line1`, `city`, `zip_code`). The CLI should accept `--line1=X --city=Y --zip-code=Z`. A custom parser keeps it dependency-free and handles the dash-to-underscore mapping trivially. Positional arguments map to the method's positional parameters in order.

**Alternatives considered**:
- **argparse** — Possible but heavy for this use case; would require dynamically building ArgumentParser per method at runtime. Not worth the complexity.
- **click** — New dependency; overkill for parameter forwarding.

## Decision 4: Output Formatting

**Decision**: Print JSON responses to stdout with 2-space indentation. Pydantic models are serialized via `.model_dump(by_alias=True, mode="json")`. Raw dicts/lists are printed via `json.dumps(indent=2)`. Primitive types (str, int, bool) are printed directly.

**Rationale**: Consistent with how the ExampleRunner formats output. JSON output is pipeable (`ab addr validate | jq .isValid`). The `by_alias=True` flag preserves API field names (camelCase) which is what users expect from a CLI tool.

**Alternatives considered**:
- **Pretty-print Python objects** — Rejected: not machine-readable, inconsistent with API field names.
- **Table format** — Rejected: complex to implement for nested objects; JSON is universally understood.

## Decision 5: Shared Aliases Module

**Decision**: Extract the `ALIASES` dict from `examples/__main__.py` into a shared location (`ab/cli/aliases.py`) that both `ex` and `ab`/`abs` import. This prevents duplication and ensures parity.

**Rationale**: FR-002 requires the same aliases in both CLIs. A shared module is the simplest way to ensure they stay in sync. The `ex` CLI's `__main__.py` will import from the shared location.

**Alternatives considered**:
- **Duplicate the dict** — Rejected: violates DRY, will drift.
- **Import from examples in the CLI** — Rejected: wrong dependency direction (SDK should not depend on examples).

## Decision 6: Method Invocation for Path Parameters

**Decision**: Use `inspect.signature()` to identify positional parameters (those without defaults) as path parameters. These are passed as positional CLI arguments. Keyword-only parameters (with `*` separator) become `--flag` arguments.

**Rationale**: ABConnect endpoint methods follow a consistent pattern:
- Path params are positional: `def get(self, job_display_id: int)`
- Query params are keyword-only: `def validate(self, *, line1=None, city=None)`
- Request bodies use `data: dict` or `**kwargs`

This convention maps cleanly to: `ab jobs get 2000000` (positional) and `ab addr validate --line1=X --city=Y` (flags).

**Alternatives considered**:
- **All params as flags** — Rejected: verbose for simple lookups (`ab jobs get --job-display-id=2000000` vs `ab jobs get 2000000`).
- **Inspect Route for path params** — Possible but requires mapping method→Route which isn't directly exposed.

## Decision 7: Authentication Failure Handling

**Decision**: Catch `FileNotFoundError` (missing .env file) and authentication errors from `ABConnectAPI.__init__()` and print a user-friendly message indicating which env file is needed. Do not attempt credential setup — just inform and exit with status 1.

**Rationale**: The CLI is a thin wrapper around the SDK. Credential management is the user's responsibility. Clear error messages pointing to `.env` or `.env.staging` are sufficient.

## Decision 8: Progress Report Housekeeping Scope

**Decision**: Regenerate `progress.html` with current data as part of this feature branch. Do not attempt to fix gate failures that require model changes or new fixtures — those are separate feature cycles. Only fix issues found in the report generation pipeline itself (rendering bugs, stale data).

**Rationale**: The test suite is green (232/0/73), Sphinx builds, and ruff passes. The 349 gate-fail markers in progress.html reflect endpoints still needing model work — that's expected ongoing work, not a bug to fix in this PR.
