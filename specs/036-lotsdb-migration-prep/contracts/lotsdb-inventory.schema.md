# Contract — Lotsdb Call-Site Inventory Schema

**Location**: `/opt/pack/ab/specs/036-lotsdb-migration-prep/lotsdb-inventory.md`
**Producer**: Manual walk-through driven by a fresh `grep -rn "ABConnect" /src/lotsdb` at execution time.
**Consumer**: Lotsdb engineer preparing the cutover PR.

## Format

Markdown document with one H2 per Lotsdb file, then a table of rows matching the `InventoryRow` entity from `data-model.md`.

```markdown
## `src/catalog/services.py`

| Line | Category | Old | New | Action | Guide anchor | Tiebreaker | Notes |
|---|---|---|---|---|---|---|---|
| 6 | import | `from ABConnect import ABConnectAPI` | `from ab import ABConnectAPI` | rewrite | `#package-rename` | none | |
| 22 | call | `ABConnectAPI(request=request, username=username, password=password)` | `ABConnectAPI(request=request)` + env-driven credentials | rewrite | `#constructor` | server | credentials must move to env file loaded at startup |
```

## Rules

- Every row’s `Guide anchor` MUST exist in `ab_migrate.md`.
- `Action == block` rows must include a linked `Known gaps` bullet in the guide.
- The inventory MUST be regenerated at execution time; this schema is only the contract, not the data.
- Grep command used to produce the inventory MUST be recorded at the top of the file for reproducibility.

## Success criteria hooks

- SC-005 is satisfied when every line returned by the grep command appears in exactly one inventory row.
- SC-001 is satisfied when a reviewer can mechanically apply every row with `action == rewrite` and get a compiling Lotsdb tree.
