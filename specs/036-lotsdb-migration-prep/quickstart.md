# Quickstart — Lotsdb Migration Prep

**Feature**: 036-lotsdb-migration-prep
**Audience**: The engineer executing Phase 3 on branch `036-lotsdb-migration-prep`.

This is a recipe, not a spec. The authoritative rules live in `spec.md`, `plan.md`, and the `contracts/` directory.

## 0. Prereqs

- Branch `036-lotsdb-migration-prep` checked out.
- `/opt/pack/ABConnectTools/` and `/src/ABConnect/` (server source) present — confirmed at plan time.
- `/src/lotsdb/` present.
- Swagger snapshots present at `/opt/pack/ABConnectTools/ABConnect/base/`.

## 1. Run the audit (once it exists)

```bash
cd /opt/pack/ab
python scripts/audit_lotsdb_migration.py --json > specs/036-lotsdb-migration-prep/audit.json
python scripts/audit_lotsdb_migration.py --markdown > specs/036-lotsdb-migration-prep/audit.md
```

Expected on first run: non-zero exit with a list of gaps.
Expected before merge: exit 0, `summary.migration_ready == true`.

## 2. Close fixture gaps

For each `gaps[]` entry with `kind == missing_*_fixture`:

1. Open the matching example under `examples/` (or create one if absent, per constitution Principle II).
2. Run the example against staging.
3. Commit the captured fixture under `tests/fixtures/requests/` (or `tests/fixtures/` for responses).
4. Re-run the audit.

Do **not** fabricate JSON. Audit should also catch fabricated fixtures via model validation on `extra="forbid"`.

## 3. Upgrade any stubs

For each `summary.stub_methods > 0`:

1. Read the server controller in `/src/ABConnect/ACPortal/…` or `/src/ABConnect/ABC.WebAPI/…` to confirm the real verb + path + body.
2. Consult swagger snapshot for parameter names.
3. Consult `ABConnectTools` implementation only as a last tiebreaker.
4. Replace the stub with a real HTTP call via the shared client.
5. Re-run the audit.

## 4. Regenerate the Lotsdb inventory

```bash
grep -rn "ABConnect" /src/lotsdb/src /src/lotsdb/pyproject.toml > /tmp/lotsdb-abconnect.txt
```

For each line in the output, add a row to `specs/036-lotsdb-migration-prep/lotsdb-inventory.md` following the schema in `contracts/lotsdb-inventory.schema.md`. Record the grep command at the top of the file for reproducibility.

## 5. Write `ab_migrate.md`

Follow the section order and style rules in `contracts/ab-migrate.outline.md`. Every row in the inventory must have a resolvable anchor in this file.

Minimum entries (confirmed during Phase 0 research — already documented in `research.md` §R3):

- Package rename `ABConnect → ab`
- Removed helpers: `FileLoader`, `APIRequestBuilder`, `Quoter`
- Removed model aliases: `ABConnect.models.*`, `ABConnect.routes.*`
- Removed exceptions: `NotLoggedInError`, `LoginFailedError`
- `ABConnectError` lost attributes: `code`, `details`, `to_dict()`, `no_traceback()`
- `RequestError` signature narrowed
- `ABConnectAPI.__init__` no longer accepts `username=` / `password=`
- Lot models moved: `ABConnect.api.models.catalog.*` → `ab.api.models.lots.*` (verify `LotCatalogDto`)

## 6. Final verification

```bash
cd /opt/pack/ab
python scripts/audit_lotsdb_migration.py       # exits 0
pytest tests/test_migration_audit.py           # green
pytest tests/swagger/test_coverage.py          # green (ensures no regressions)
pytest                                          # full suite, green
```

Every row in `lotsdb-inventory.md` must link to a real anchor in `ab_migrate.md`. Every `GuideEntry` with a behavior change must carry a tiebreaker source.

## 7. Hand-off

Commit as a checkpoint per Principle VIII. Open a PR titled `docs(migration): prepare lotsdb migration from ABConnectTools to ab`. Lotsdb cutover itself is **out of scope** — it happens in a separate PR in the Lotsdb repo using `ab_migrate.md` + `lotsdb-inventory.md` as the execution checklist.
