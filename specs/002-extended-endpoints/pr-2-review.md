# PR #2 Review (local branch: `002-extended-endpoints` vs `main`)

## Findings

1. **Medium**: Fixture validation tests now skip on missing fixtures, which can hide regression in model coverage.
- `tests/conftest.py:29` introduces `require_fixture(...)` that calls `pytest.skip(...)` when a fixture file is absent.
- Existing model tests switched from hard fixture loads to skip-on-missing behavior.
- Impact: deleting/losing a fixture no longer fails model tests, so schema drift can silently reduce test signal while CI remains green.
- Suggested fix: keep skip behavior only for explicitly new/pending models, but require failure for previously captured/required fixtures.
- **Resolution**: Added `required=True` parameter to `require_fixture()`. Tests with `@pytest.mark.live` (captured fixtures) now FAIL if fixture is missing. Pending fixtures still skip.

## Verification Notes

- `pytest -q tests/models tests/test_mock_coverage.py`: passed (26 passed, 27 skipped).
