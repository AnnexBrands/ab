# Repository Guidelines

## Project Structure & Module Organization
- `ab/`: SDK source code.
  - `ab/api/endpoints/`: endpoint groups by API surface.
  - `ab/api/models/`: Pydantic request/response models.
  - `ab/client.py`: top-level `ABConnectAPI` facade.
- `tests/`: pytest suite.
  - `tests/models/`: fixture-backed model validation.
  - `tests/integration/`: live API tests (staging credentials required).
  - `tests/fixtures/`: real JSON fixtures, tracked in `FIXTURES.md`.
- `examples/`: runnable endpoint usage scripts.
- `docs/`: Sphinx docs (`docs/Makefile`, `index.md`, `api/`, `models/`).
- `specs/`: feature specs and delivery artifacts.

## Build, Test, and Development Commands
- `pip install -e .`: install SDK in editable mode.
- `pip install -e .[dev,docs]`: install lint/test/docs tooling.
- `pytest tests/ --ignore=tests/integration -v`: fast local suite.
- `pytest tests/integration/ -m live -v`: live staging checks.
- `ruff check .`: lint imports/style/errors.
- `cd docs && make html`: build documentation.

## Coding Style & Naming Conventions
- Python 3.11+; 4-space indentation; max line length 120 (Ruff).
- Use `snake_case` for functions/variables, `PascalCase` for classes.
- Endpoint methods should map directly to HTTP behavior (`get_*`, `create_*`, `update_*`, `delete_*`).
- Models must inherit shared bases (`RequestModel`/`ResponseModel`) and use explicit field aliases when API keys differ.

## Testing Guidelines
- Framework: `pytest` with markers `live` and `mock` (legacy marker may still exist).
- Test files: `tests/**/test_*.py`; test names: `test_<behavior>()`.
- New/changed endpoints require:
  - model validation test,
  - integration test when safe,
  - fixture status update in `FIXTURES.md`.
- Prefer real captured fixtures; avoid fabricated data.

## Commit & Pull Request Guidelines
- Follow existing commit style: `feat(scope): summary` (e.g., `feat(sdk): extend shipment endpoints`).
- Keep commits focused and atomic; include tests/docs updates with code changes.
- PRs should include:
  - clear summary and rationale,
  - linked spec folder (for example `specs/002-extended-endpoints/`),
  - test evidence (`pytest`/`ruff` results),
  - fixture/doc updates when endpoint contracts change.

## Coexisting Agents
  Claude (using speckit commands) handle planning and implementation
- Codex is only to write PR at end of implementation cycle