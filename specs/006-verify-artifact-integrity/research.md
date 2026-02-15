# Research: Verify Artifact Integrity

## R1: What artifacts track endpoint status?

**Decision**: Three primary sources of truth exist, plus ground-truth
directories:

| Artifact | Tracks | Format |
|----------|--------|--------|
| `FIXTURES.md` | Fixture capture status | Markdown table: captured vs needs-request-data |
| `specs/api-surface.md` | Implementation status | Markdown table: done/pending/not-started per endpoint |
| `examples/*.py` | Example entries | `runner.add()` calls with optional `fixture_file` param |
| `tests/fixtures/*.json` | Actual fixture files | JSON files on disk |
| `progress.html` | Generated report | HTML from `scripts/generate_progress.py` |

**Rationale**: All five must agree. Ground truth is:
fixture files on disk + live example output.

## R2: How to run examples programmatically?

**Decision**: Use the existing `ExampleRunner` framework. Each
`examples/{module}.py` has a `runner` attribute with `.run()` method.
The unified dispatcher (`python -m examples {module}`) can run all
entries for a module or individual entries.

**Approach**: Run each module one at a time, capture stdout/stderr,
check for HTTP errors and warnings. The runner already prints
results and handles exceptions.

**Alternative considered**: Write a new test harness — rejected
because the runner framework already exists and handles auth,
error reporting, and fixture saving.

## R3: What counts as a "passing" example?

**Decision**: An example passes if:
1. No Python exception raised
2. No HTTP error (4xx/5xx) returned
3. No warning messages printed to stderr
4. For entries with `fixture_file`: the named file exists in
   `tests/fixtures/`

An example is "expected to fail" if it has a `# TODO` comment
indicating it needs request data. These are not counted as
discrepancies.

## R4: What cross-reference checks are needed?

**Decision**: Four consistency checks:

1. **Fixture file → FIXTURES.md**: Every `.json` file in
   `tests/fixtures/` must appear as "captured" in FIXTURES.md.
2. **FIXTURES.md captured → fixture file**: Every "captured"
   entry in FIXTURES.md must have a corresponding file on disk.
3. **Example fixture_file → disk**: Every `runner.add()` with
   `fixture_file="X.json"` must have `tests/fixtures/X.json`
   on disk.
4. **api-surface.md done → example exists**: Every endpoint
   marked "done" must have a `runner.add()` entry.

## R5: How to correct discrepancies?

**Decision**: Manual edits to tracking documents:
- FIXTURES.md: Move entries between captured/needs-request-data
  tables, update summary counts.
- api-surface.md: Change status markers for failed endpoints.
- Regenerate progress.html: Run `python scripts/generate_progress.py`.
