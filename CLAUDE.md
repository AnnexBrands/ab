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
- Python 3.11+ (unchanged from 001) + pydantic>=2.0, pydantic-settings, requests, python-dotenv (unchanged from 001) (008-extended-operations)
- Python 3.11+ + pydantic>=2.0, pydantic-settings, requests, python-dotenv (unchanged) (009-remaining-endpoints)

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
- 009-remaining-endpoints: Added Python 3.11+ + pydantic>=2.0, pydantic-settings, requests, python-dotenv (unchanged)
- 008-extended-operations: Added Python 3.11+ (unchanged from 001) + pydantic>=2.0, pydantic-settings, requests, python-dotenv (unchanged from 001)
- 007-request-model-methodology: Added Python 3.11+ (existing SDK) + pydantic>=2.0, requests (existing SDK deps — no new dependencies)

