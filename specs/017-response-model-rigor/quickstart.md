# Quickstart: Response Model Rigor

## Scenario 1: List-wrapper unwrapping works

```python
# Before fix: returns raw dict
result = api.jobs.get_parcel_items(4675060)
# result == {"modifiedDate": "2026-...", "parcelItems": [{...}, ...]}

# After fix: returns typed list
result = api.jobs.get_parcel_items(4675060)
# result == [ParcelItem(id=1, ...), ParcelItem(id=2, ...)]
assert isinstance(result, list)
assert isinstance(result[0], ParcelItem)
```

## Scenario 2: Missing fixture_file audit

```bash
# Run the fixture completeness test
pytest tests/test_fixture_completeness.py -v

# Expected: all entries with response_model also have fixture_file
# No failures
```

## Scenario 3: Capture a fixture via example runner

```bash
# Run parcels example to capture fixtures
python -m examples.parcels get_parcel_items

# Output includes:
#   Fixture saved → tests/fixtures/ParcelItem.json

# Then run fixture validation
pytest tests/models/test_parcel_models.py -v
# All tests pass, no extra fields
```

## Scenario 4: Verify progress.html cleanup

```bash
ls progress.html 2>/dev/null || echo "Cleaned up"
# "Cleaned up"

ls html/progress.html
# html/progress.html exists
```
