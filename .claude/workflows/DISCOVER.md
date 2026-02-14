# DISCOVER Workflow v3

Phased approach for systematically implementing missing API
endpoints with example-driven fixture capture and clean context
recovery.

**Constitution**: `.specify/memory/constitution.md` v2.2.0
**Principles**: II (Example-Driven Fixture Capture),
III (Four-Way Harmony), V (Endpoint Status Tracking),
VIII (Phase-Based Context Recovery),
IX (Endpoint Input Validation)
**Endpoint inventory**: `specs/api-surface.md`

## Overview

```mermaid
flowchart TD
    D[D — Determine\nResearch params from\nABConnectTools + swagger]
    I[I — Implement models\nPydantic models + skeleton tests]
    S[S — Scaffold endpoints\nEndpoint methods + client wiring]
    C[C — Call & Capture\nExamples call methods\n200 → fixture saved]
    O[O — Observe tests\nRun suite, check harmony]
    V[V — Verify & commit\nCheckpoint commit]
    E[E — Enrich docs\nSphinx documentation]
    R[R — Release\nPR ready]
    FIX[FIX REQUEST\nResearch correct\nparams / body]
    MORE{More service\ngroups?}

    D --> I --> S --> C
    C -->|200 response| O
    C -->|error| FIX
    FIX --> C
    O --> V --> E --> R
    R --> MORE
    MORE -->|yes| D
    MORE -->|no| DONE[Done]

    style C fill:#d4edda,stroke:#155724
    style FIX fill:#fff3cd,stroke:#856404
    style R fill:#d4edda,stroke:#155724
    style DONE fill:#d4edda,stroke:#155724
```

## Phase Definitions

### D — Determine Requirements

**Entry**: Target group selected from `specs/api-surface.md`.
**Action**: Research ABConnectTools and swagger for the target
group. The goal is to know exactly what each endpoint needs
BEFORE writing an example.

For each endpoint in the group:

1. **Routes**: Read `ABConnectTools/ABConnect/api/routes.py`
   (`SCHEMA["{GROUP}"]`) for method + path.
2. **Endpoint code**: Read
   `ABConnectTools/ABConnect/api/endpoints/{service}.py` for
   method signatures — what parameters does it accept? What
   does it pass as query params vs request body vs URL params?
3. **Examples**: Read `ABConnectTools/examples/api/{service}.py`
   for realistic parameter values and usage patterns.
4. **Swagger**: Read the swagger spec for parameter definitions,
   required vs optional fields, and request/response body schemas.
   **Critically**: note the exact query parameter names and
   whether the endpoint has a `requestBody` — this determines
   transport type (Principle IX).
5. **Models**: Read `ABConnectTools/ABConnect/api/models/{service}.py`
   for field names, aliases, Optional vs required, nesting.
6. **Fixtures**: Check `ABConnectTools/tests/fixtures/{Name}.json`
   for response shapes (see Ref column in `api-surface.md`).

**Key output per endpoint**:

- HTTP method + path
- Required query parameters (with example values)
- Required request body fields (with example values)
- Required URL parameters (with example values)
- Known quirks or prerequisites

**Exit**: Understanding of what every endpoint needs. No code
written yet.
**Artifact**: Optionally note deviations in the feature's
`research.md`.

### I — Implement Models

**Entry**: Determine phase complete for target service group.
**Action**:
1. Create Pydantic models from swagger schemas + ABConnectTools
   model patterns observed in Phase D.
2. Write skeleton test files with `pytest.skip()` for each model
   that lacks a fixture.

**Exit**: Models pass `ruff check`. Tests skip cleanly.
**Artifact**: `ab/api/models/{service}.py`,
`tests/models/test_{service}_models.py`

**Skeleton test pattern**:

```python
import pytest
from tests.conftest import FIXTURES_DIR, load_fixture
from ab.api.models.{service} import {ModelName}

class Test{Service}Models:
    def test_{model_name}(self):
        fixture = FIXTURES_DIR / "{ModelName}.json"
        if not fixture.exists():
            pytest.skip(
                "Fixture needed: run examples/{service}.py — "
                "endpoint needs {what_is_missing}"
            )
        data = load_fixture("{ModelName}")
        model = {ModelName}.model_validate(data)
        assert model.id is not None
```

### S — Scaffold Endpoints

**Entry**: Models defined for target service group.
**Action**:
1. Write endpoint class methods with route definitions.
2. Register endpoint in `ab/client.py`.
3. Export from `ab/api/endpoints/__init__.py`.
4. Export models from `ab/api/models/__init__.py`.
5. Verify input validation (Principle IX): parameter names
   MUST match swagger, request bodies MUST validate against
   Pydantic `RequestModel` before sending.

**Exit**: Endpoint code passes `ruff check` and
`pytest tests/test_example_params.py`. Client registers
all new endpoints. Imports work.
**Artifact**: `ab/api/endpoints/{service}.py`, updated
`ab/client.py`, updated `__init__.py` files.

**Checkpoint commit**: At this point, commit with message:
`feat({service}): add models and endpoint scaffold (DISCOVER D-I-S)`

### C — Call & Capture

**Entry**: Endpoints scaffolded for target service group.
**Action**: Write runnable examples using the request data
researched in Phase D. Run examples against staging.

**The capture loop** (per endpoint):

1. Write example call with researched parameters (query params,
   request body, URL params).
2. Run the example.
3. **200 response** → save response as fixture in
   `tests/fixtures/{ModelName}.json`. Done.
4. **Error response** → the example has wrong or missing request
   data. Go back to Phase D research for this endpoint. Fix the
   example. Re-run. Do NOT ask for a response fixture.

**Examples go in `examples/{service}.py`**. Each example file
covers all endpoints for that service group.

**Example pattern**:

```python
"""Example: {Service} operations."""

from ab import ABConnectAPI
import json

api = ABConnectAPI(env="staging")

# {endpoint_description}
result = api.{service}.{method}(
    # Parameters researched from ABConnectTools + swagger:
    param1="realistic_value",
    param2="realistic_value",
)
print(f"{Method}: {result}")

# Save fixture (run once, then remove this block):
# with open(f"tests/fixtures/{ModelName}.json", "w") as f:
#     json.dump(result.model_dump(by_alias=True), f, indent=2)
```

**After capturing**: Update the test to remove `pytest.skip()`
and add `@pytest.mark.live`. Update `FIXTURES.md` status to
`captured`.

**Exit**: Examples exist for all endpoints. Fixtures captured
for endpoints that returned 200. Remaining endpoints tracked
as `needs-request-data` in `FIXTURES.md` with specifics.
**Artifact**: `examples/{service}.py`,
`tests/fixtures/{ModelName}.json` (for captured endpoints)

**Commit message**:
`feat({service}): add examples and capture fixtures (DISCOVER C)`

### O — Observe Tests

**Entry**: Examples written and fixtures captured (where possible)
for target service group.
**Action**:
1. Run `pytest tests/models/test_{service}_models.py -v`.
2. Check for extra-field warnings (model drift detection).
3. Verify Four-Way Harmony checklist for each endpoint.

**Exit**: All tests pass (captured) or skip with actionable
messages (needs-request-data). No unexpected failures.
**Artifact**: Passing test output.

**Four-Way Harmony checklist** (per endpoint):

- [ ] `ab/api/endpoints/{service}.py` — method exists
- [ ] `ab/api/models/{service}.py` — model exists
- [ ] `examples/{service}.py` — example exists with correct params
- [ ] `tests/fixtures/{ModelName}.json` — fixture captured (or
      status tracked in `FIXTURES.md`)
- [ ] `tests/models/test_{service}_models.py` — test passes or
      skips with actionable message
- [ ] `docs/` — documentation exists (Phase E)

### V — Verify & Commit

**Entry**: Tests pass for target service group.
**Action**:
1. Update `FIXTURES.md`:
   - Captured endpoints → `captured` with date and source.
   - Endpoints still failing → `needs-request-data` with
     specifics on what params/body are missing.
2. Update `specs/api-surface.md` — mark endpoints as done.
3. Run full test suite: `pytest --tb=short`.
4. Commit checkpoint.

**Exit**: Clean git state. `FIXTURES.md` current. No generic
"pending" statuses — every non-captured endpoint specifies
what request data is missing.
**Artifact**: Git commit.

**Commit message**:
`feat({service}): verify models and update tracking (DISCOVER O-V)`

### E — Enrich Documentation

**Entry**: Fixtures verified for target service group.
**Action**:
1. Write Sphinx documentation page.
2. Final Four-Way Harmony audit.

**Exit**: Docs build without warnings.
**Artifact**: `docs/{service}.rst`

**Commit message**:
`docs({service}): add documentation (DISCOVER E)`

### R — Release

**Entry**: All DISCOVER phases complete for the batch.
**Action**:
1. Final `pytest` run (full suite).
2. `ruff check .` passes.
3. Update `specs/api-surface.md` status columns.
4. PR ready.

**Exit**: Branch ready for PR to main.

## Batching Strategy

Work in service groups of 5–15 endpoints. Each batch completes
all DISCOVER phases before starting the next.

### Grouping Rules

1. **By API surface**: ACPortal, Catalog, ABC.
2. **By domain**: See `specs/api-surface.md` groups.
3. **By request complexity**: Groups where ABConnectTools has
   examples with realistic parameter values are faster to
   implement — prioritize these.
4. **By priority**: Stakeholder-driven (Principle VII).

### Recommended Batch Order

See `specs/api-surface.md` § Batch Planning for current
prioritized batch list.

## Resuming Work

When entering a new context (new session, context overflow
recovery, or handoff to a different agent):

### Step 1: Read this workflow

```
Read .claude/workflows/DISCOVER.md
```

### Step 2: Check the endpoint inventory

```
Read specs/api-surface.md
```

### Step 3: Check git state

```bash
git log --oneline -20
git status
git diff --stat
```

### Step 4: Check endpoint status

```bash
# Count by status
grep -c "captured" FIXTURES.md
grep -c "needs-request-data" FIXTURES.md
```

### Step 5: Run tests to see current state

```bash
pytest --tb=line -q 2>&1 | tail -20
```

### Step 6: Identify current phase

Look at the last commit message for DISCOVER phase markers
(e.g., `DISCOVER D-I-S` means phases D, I, S are done —
resume at phase C).

### Step 7: Resume

Pick up from the next incomplete phase. Do NOT restart from
scratch. All prior phase artifacts are committed and valid.

## ABConnectTools Reference Paths

Quick lookup for Phase D:

| What | Path |
|------|------|
| All routes | `/usr/src/pkgs/ABConnectTools/ABConnect/api/routes.py` |
| Models | `/usr/src/pkgs/ABConnectTools/ABConnect/api/models/{service}.py` |
| Endpoints | `/usr/src/pkgs/ABConnectTools/ABConnect/api/endpoints/{service}.py` |
| Job sub-endpoints | `/usr/src/pkgs/ABConnectTools/ABConnect/api/endpoints/jobs/{sub}.py` |
| Fixtures (JSON) | `/usr/src/pkgs/ABConnectTools/tests/fixtures/{Name}.json` |
| Fixtures (PDF) | `/usr/src/pkgs/ABConnectTools/tests/fixtures/{Name}.pdf` |
| Examples | `/usr/src/pkgs/ABConnectTools/examples/api/{service}.py` |

## Anti-Patterns

- **Fabricating fixtures**: Never invent JSON data. If the
  example errors, fix the request. Research ABConnectTools and
  swagger to find the correct params/body.
- **Asking for response fixtures when the request is wrong**:
  A 400 error means the example needs correct parameters, not
  that a human needs to provide a response. Research
  ABConnectTools and swagger to find the right request data.
- **Unvalidated inputs**: Endpoint methods MUST validate
  inputs against Pydantic models and swagger param names before
  making HTTP calls. Guessed parameter names (e.g., `street`
  instead of swagger's `Line1`) are silently ignored by the
  API. Request bodies sent as `params=` instead of `json=`
  are silently dropped. `tests/test_example_params.py` catches
  these automatically (Principle IX).
- **Writing examples without research**: Phase D exists for a
  reason. Every example MUST use parameters researched from
  ABConnectTools endpoint code, examples, and swagger specs.
- **Copying from ABConnectTools**: Phase D is read-only.
  Understand patterns, then implement clean-room with our
  stricter standards (extra="forbid"/"allow", drift logging,
  mixin inheritance).
- **Generic "pending" status**: Every non-captured endpoint
  MUST specify `needs-request-data` with details on what's
  missing. Never use a vague "pending."
- **Skipping phases**: Every phase produces artifacts. Skipping
  a phase leaves gaps that compound.
- **Re-discovering endpoints**: The endpoint inventory lives in
  `specs/api-surface.md`. Never re-parse swagger to find gaps.
- **Giant batches**: Keep batches to 5–15 endpoints. Larger
  batches risk context overflow before reaching Phase V
  (checkpoint commit).
- **Uncommitted multi-phase work**: Always commit at Phase V.
  If context is lost before V, all work since the last commit
  is gone.
