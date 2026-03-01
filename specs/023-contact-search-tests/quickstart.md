# Quickstart: Contact Search Tests

## Verify in 3 steps

### 1. Run the new contact search tests

```bash
pytest tests/models/test_contact_search.py -v
```

Expected: All tests pass (18 test cases — 12 passing permutations + 3 failing permutations + 3 extra-field rejections + response tests).

### 2. Run the full test suite for regressions

```bash
pytest tests/ -x -q -m "not live"
```

Expected: 413+ passed (current baseline), 0 failures, no regressions.

### 3. Regenerate progress report

```bash
python scripts/generate_progress.py
```

Expected: `html/progress.html` regenerated. Open in browser and confirm `/contacts/v2/search` shows as complete with all gates PASS.
