# Baseline — 037-example-coverage

**Captured**: 2026-06-06 (start of implementation)

## Non-live test suite (`pytest -m "not live"`)

```
903 passed, 40 skipped, 78 deselected, 5 xfailed in ~5.7s
```

This is the green starting state (matches the quality baseline of 903/0). Any
regression in this number during feature work must be explained.

## Report generation

`python scripts/generate_progress.py` renders `html/progress.html` and the no-drift
gate (`is_report_current()`) is satisfied at start.

## Pytest markers (already present in pyproject.toml)

- `mock: tests backed by mock/fabricated fixtures`
- `live: tests backed by live-captured fixtures`

→ **T001 satisfied**: the `live` marker exists; `pytest -m "not live"` runs cleanly.

## Example coverage (pre-feature, from the noisy scanner)

~209 routed methods / 36 endpoint classes. Whole `jobs.*` subgroups (email, sms,
on_hold, payment, shipment, note, freight_providers, parcel_items, rfq, status,
tracking, form) have zero examples. The precise `example_index` (T005) will produce
the authoritative gap list (T009).
