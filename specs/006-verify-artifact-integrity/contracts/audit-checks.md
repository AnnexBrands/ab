# Audit Checks Contract

## Check 1: Fixture Files Match FIXTURES.md

**Input**: `tests/fixtures/*.json` + FIXTURES.md captured table
**Rule**: Sets must be equal (bidirectional)

- Every `.json` file on disk → row in captured table
- Every captured row → `.json` file on disk
- **Finding if**: file on disk not in table, or table entry not on disk

## Check 2: Captured Fixtures Parse Against Models

**Input**: `tests/fixtures/*.json` + `ab/api/models/*.py`
**Rule**: Each fixture file must parse against its named model

- Load fixture JSON
- Call `ModelName.model_validate(data)` (or validate list items)
- **Finding if**: ValidationError raised

## Check 3: Examples Run Without Errors

**Input**: `examples/*.py` runner entries
**Rule**: Entries with `fixture_file` must succeed against staging

- Run each entry
- Check: no exception, no HTTP error, no warning
- **Finding if**: any failure for an entry claimed as captured

## Check 4: Example fixture_file References Exist

**Input**: `examples/*.py` runner.add() calls with `fixture_file` param
**Rule**: Named file must exist in `tests/fixtures/`

- Parse `fixture_file="X.json"` from each entry
- Check `tests/fixtures/X.json` exists
- **Finding if**: file missing

## Check 5: api-surface.md Done Entries Have Examples

**Input**: `specs/api-surface.md` done entries + `examples/*.py`
**Rule**: Every done endpoint has a runner.add() entry

- Parse done endpoints from api-surface.md
- Search examples for matching runner.add() entry
- **Finding if**: no example for a done endpoint

## Check 6: FIXTURES.md Summary Counts Match

**Input**: FIXTURES.md summary section + table row counts
**Rule**: Summary counts = actual row counts

- Count rows in captured table
- Count rows in needs-request-data table
- Compare against summary bullets
- **Finding if**: counts disagree
