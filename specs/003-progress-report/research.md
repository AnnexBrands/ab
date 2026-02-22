# Research: Progress Report

**Feature**: 003-progress-report
**Date**: 2026-02-14

## R1: Markdown Table Parsing Strategy

**Decision**: Regex-based line-by-line parsing using Python `re` module.

**Rationale**: The `api-surface.md` tables follow a rigid, consistent format:
- Pipe-delimited columns with fixed headers (`| # | Route Key | Method | Path | Response Model | AB | Ref |`)
- Status values are a small closed set: `done`, `pending`, `—`
- Section headers (`### GroupName`) delimit endpoint groups
- API surface sections (`## Endpoint Groups — ACPortal/Catalog/ABC`) delimit surfaces

The format is machine-generated and maintained by the SDK team, so it won't drift unpredictably. A regex parser is simpler, faster, and has zero dependencies compared to a full markdown AST parser.

**Alternatives considered**:
- `markdown-it-py` or `mistune`: Full markdown AST parsing. Adds external dependency for no benefit — we only need table rows and headers, not arbitrary markdown.
- `pandas.read_csv` with pipe delimiter: Overkill, heavyweight dependency for simple tabular extraction.

**Parsing patterns**:
- Endpoint table row: `^\| \d+ \|` (starts with pipe + number)
- Group header: `^### (.+)` under `## Endpoint Groups — (ACPortal|Catalog|ABC)`
- AB status column: 6th pipe-delimited field, values: `done`, `pending`, `—`
- Group summary: `**Total**: N | **AB done**: M`

## R2: FIXTURES.md Parsing Strategy

**Decision**: Same regex approach, two separate table sections.

**Rationale**: `FIXTURES.md` has two clearly labeled sections:
- `## Captured Fixtures` — table with `| Endpoint Path | Method | Model Name | Date | Source | ABConnectTools Ref |`
- `## Pending Fixtures` — table with `| Endpoint Path | Method | Model Name | Capture Instructions | Blocker | ABConnectTools Ref |`

Both use consistent column headers. Parse each section independently.

**Key fields to extract**:
- Pending: model name, endpoint path, method, capture instructions, blocker reason
- Captured: model name, endpoint path, method (for cross-reference with api-surface)

## R3: Constants Detection

**Decision**: Regex scan of `tests/constants.py` for `TEST_*` assignments.

**Rationale**: Constants file is simple — flat module with `NAME = value` assignments. Pattern: `^(TEST_\w++)\s*=`. No need to import or execute the file.

**Cross-reference strategy**: The pending fixtures in `FIXTURES.md` describe blockers like "Needs job with shipment tracking". Map these to required constants:
- Endpoint paths containing `{id}` or `{jobDisplayId}` → need `TEST_JOB_DISPLAY_ID`
- Endpoint paths containing `{companyId}` → need `TEST_COMPANY_UUID`
- Endpoint paths containing `{contactId}` → need `TEST_CONTACT_ID`
- Endpoint paths containing `{sourceId}`, `{shipmentId}`, etc. → need new constant (flag in instructions)

## R4: HTML Generation Approach

**Decision**: Python string templates with inline CSS. No template engine.

**Rationale**: The HTML is a single file with a fixed structure (header, summary table, action-required sections). Python f-strings and `html.escape()` are sufficient. Inline CSS keeps the file self-contained per FR-001.

**Alternatives considered**:
- Jinja2: Adds external dependency. Template files add deployment complexity for a single-file output.
- `string.Template`: Weaker than f-strings, no real advantage.

**Design**:
- CSS in `<style>` block at top of HTML
- Summary section: HTML table with color-coded cells (green=done, yellow=pending, gray=not started)
- Action Required section: Collapsible `<details>` elements per endpoint group, with instruction steps as ordered lists
- Responsive layout for readability

## R5: Instruction Generation Logic

**Decision**: Template-based instruction builder keyed on blocker type.

**Rationale**: The pending fixtures have a small set of blocker categories:
1. **Fixture capture possible** — endpoint is scaffolded, just needs human to call it
2. **New constant needed** — endpoint requires an entity ID not yet in constants.py
3. **Environment blocked** — staging doesn't have the required data
4. **Not started** — no models or endpoint code exists yet

Each category gets a distinct instruction template:
- Category 1: "Run `api.{service}.{method}(...)`, save to `tests/fixtures/{Model}.json`, run `pytest tests/... -k test_{model}`"
- Category 2: Same as 1, but prepend "Add `TEST_{NAME} = <value>` to `tests/constants.py`"
- Category 3: "Blocked: {reason}. Options: capture from production, request data setup, or defer."
- Category 4: "Implementation needed: create model in `ab/api/models/`, endpoint in `ab/api/endpoints/`, skeleton test. Then capture fixture."

**Source for SDK method names**: The `Capture Instructions` column in `FIXTURES.md` already contains SDK method calls (e.g., `api.jobs.get_timeline(job_id)`). For not-started endpoints, generate a suggested method name from the route key.
