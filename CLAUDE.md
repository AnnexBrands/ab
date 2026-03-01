# AB Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-13

## Active Technologies
- Python 3.11+ + pydantic>=2.0, pydantic-settings, requests, python-dotenv (unchanged from 001) (002-extended-endpoints)
- N/A (SDK — no local storage) (002-extended-endpoints)
- Python 3.11+ (same as SDK) + None beyond stdlib (`re`, `pathlib`, `html`, `json`, `datetime`) (003-progress-report)
- N/A — reads existing files, writes a single HTML file (003-progress-report)
- Python 3.11+ + pydantic>=2.0, requests (existing SDK deps — no new dependencies) (004-scaffold-examples-fixtures)
- Filesystem (fixture JSON files in `tests/fixtures/`) (004-scaffold-examples-fixtures)
- Python 3.11+ (existing SDK) + pydantic>=2.0, requests (existing SDK deps) (006-verify-artifact-integrity)
- Python 3.11+ (existing SDK) + pydantic>=2.0, requests (existing SDK deps — no new dependencies) (007-request-model-methodology)
- Filesystem (fixture JSON files in `tests/fixtures/` and `tests/fixtures/requests/`) (007-request-model-methodology)
- N/A — documentation-only change (Markdown files) + N/A — no code dependencies (010-update-constitution)
- Python 3.11+ (existing SDK) + pydantic>=2.0, requests, sphinx, sphinx-rtd-theme, myst-parser (all existing) (011-endpoint-quality-gates)
- Filesystem (fixture JSON files in `tests/fixtures/`, generated Markdown/HTML) (011-endpoint-quality-gates)
- Filesystem (fixture JSON files in `tests/fixtures/` and `tests/fixtures/mocks/`) (013-test-mock-framework)
- Python 3.11+ (existing SDK) + pydantic>=2.0, requests (existing SDK deps — no new dependencies) (014-endpoint-cli)
- Filesystem (fixture JSON files in `tests/fixtures/requests/`) (015-endpoint-request-mocks)
- N/A — SDK, no local storage (018-job-get-response)
- N/A (SDK — no persistence) (019-refine-request-models)
- Python 3.11+ + pydantic>=2.0, requests (existing SDK) + pydantic>=2.0, requests (no new deps) (021-endpoint-quality-sweep)

- Python 3.11+ + pydantic>=2.0, pydantic-settings, requests, python-dotenv (001-abconnect-sdk)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.11+: Follow standard conventions

## Recent Changes
- 023-contact-search-tests: Added Python 3.11+ (existing SDK) + pydantic>=2.0, requests (existing SDK deps — no new dependencies)
- 022-fix-contact-search: Added Python 3.11+ + pydantic>=2.0, requests (existing SDK) + pydantic>=2.0, requests (no new deps)
- 021-endpoint-quality-sweep: Added Python 3.11+ + pydantic>=2.0, requests (existing SDK) + pydantic>=2.0, requests (no new deps)

