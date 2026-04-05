# Phase 1 Data Model — Lotsdb Migration Prep

**Feature**: 036-lotsdb-migration-prep
**Date**: 2026-04-04

This feature produces documentation, not runtime data. The "data model" here is the shape of the three structured artifacts (audit record, inventory row, migration-guide entry). These shapes are the contracts the audit script and the reviewer consume.

## Entity 1 — `AuditRecord` (one per public endpoint method)

| Field | Type | Description |
|---|---|---|
| `module` | string | Python module under `ab.api.endpoints` (e.g. `"jobs"`). |
| `class_name` | string | Endpoint class (e.g. `"JobsEndpoint"`). |
| `method_name` | string | Public method (e.g. `"get_by_display_id"`). |
| `http_verb` | `GET\|POST\|PUT\|PATCH\|DELETE` | HTTP verb extracted from the route decorator or client call. |
| `route_path` | string | Path template (e.g. `/job/{jobDisplayId}`). |
| `api_surface` | `acportal\|catalog\|abc` | Which upstream base URL this hits. |
| `has_path_params` | bool | True if the route template contains `{…}`. |
| `has_query_params` | bool | True if the method binds any `params=` values. |
| `has_body` | bool | True if the method accepts a `RequestModel` body. |
| `body_model` | string \| null | Dotted name of the request body model, if any. |
| `params_model` | string \| null | Dotted name of a `Params` model, if the method uses one. |
| `path_param_fixture` | `present\|na\|missing` | `na` when the route takes no path params. |
| `query_fixture` | `present\|na\|missing` | `na` when there are no query params. |
| `body_fixture` | `present\|na\|missing` | `na` when there is no body. |
| `calls_real_api` | bool | True if method body invokes an HTTP client method on `self`. |
| `stub_reason` | string \| null | Populated when `calls_real_api == False`. |
| `notes` | string \| null | Free-text caveats (e.g. "swagger silent, tiebreaker ABConnectTools"). |

**Invariants**:

- If `has_body == True` then `body_model != null`.
- If `calls_real_api == False` then `stub_reason != null` and the endpoint blocks migration-ready state.
- `*_fixture == "missing"` on any non-`na` category blocks migration-ready state.

**State transitions** (reviewer workflow):

```
collected → gaps_identified → gaps_closed → migration_ready
                              ↑
                              │ fix stub / capture fixture / correct model
                              │
                        back to collected on re-run
```

## Entity 2 — `InventoryRow` (one per `ABConnect`-referencing line in `/src/lotsdb`)

| Field | Type | Description |
|---|---|---|
| `file` | string | Path relative to `/src/lotsdb` (e.g. `src/catalog/services.py`). |
| `line` | int | Line number of the reference. |
| `old_text` | string | Exact source line as it exists today. |
| `category` | `import\|call\|type\|string` | What kind of reference this is. |
| `new_text` | string \| null | Exact replacement line for the `ab` port. Null when `action == "remove"`. |
| `action` | `rewrite\|remove\|block\|no_change` | `block` = a break the guide cannot yet resolve; cutover is blocked until resolved. |
| `guide_anchor` | string | Anchor in `ab_migrate.md` that explains this rewrite (e.g. `#exceptions-removed`). |
| `tiebreaker_used` | `server\|fixture\|swagger\|abconnecttools\|none` | Which source resolved any ambiguity. |
| `notes` | string \| null | Free-text. |

**Invariants**:

- Every row MUST reference a section of `ab_migrate.md` via `guide_anchor`, except rows with `action == "no_change"`.
- `action == "block"` rows MUST list at least one unresolved Tier-1/Tier-2 question in `notes`.

## Entity 3 — `GuideEntry` (one per backward-incompatible change in `ab_migrate.md`)

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable slug used as the markdown anchor (e.g. `package-rename`). |
| `area` | `package\|exception\|constructor\|model\|endpoint\|helper\|auth\|dependency` | Classification. |
| `summary` | string | One-line description of the break. |
| `before` | code block | Representative `ABConnectTools` usage. |
| `after` | code block \| null | Representative `ab` replacement, or null if no direct replacement exists. |
| `rationale` | string | Why the break exists (rename, cleanup, model relocation, etc.). |
| `silent` | bool | True if the break is a silent regression (imports resolve, behavior degrades). |
| `affected_lotsdb_files` | list[string] | Files in `InventoryRow.file` touched by this entry. |
| `tiebreaker` | `server\|fixture\|swagger\|abconnecttools\|none` | Which source resolved any behavior question. |

**Invariants**:

- Every `InventoryRow.guide_anchor` MUST resolve to a `GuideEntry.id`.
- `silent == True` entries MUST include at least one `after` snippet that preserves the original information (e.g. how to log the former `ABConnectError.details`).

## Entity 4 — `ExportMap` (one row per `ABConnectTools` public symbol)

| Field | Type | Description |
|---|---|---|
| `symbol` | string | Fully qualified `ABConnect.*` dotted path (e.g. `ABConnect.api.models.catalog.AddLotRequest`). |
| `kind` | `class\|function\|module_alias\|constant` | |
| `ab_equivalent` | string \| null | Fully qualified `ab.*` path, or null. |
| `status` | `kept\|renamed\|moved\|removed\|oos` | `oos` = out-of-scope for migration (e.g. `Quoter`). |
| `lotsdb_used` | bool | True if at least one `InventoryRow` references this symbol. |
| `guide_entry_id` | string \| null | Link back to `GuideEntry.id`. |

**Invariant**: Every row with `lotsdb_used == True` MUST have a non-null `guide_entry_id`. Rows with `status == "removed"` and `lotsdb_used == True` MUST map to either a `GuideEntry` with a replacement pattern or an `InventoryRow.action == "block"`.

## Derived metrics (for Success Criteria)

- **SC-002** satisfied ⇔ every `AuditRecord` has no `missing` in any category.
- **SC-003** satisfied ⇔ every `AuditRecord.calls_real_api == True`.
- **SC-004** satisfied ⇔ `ExportMap` has an entry for every public symbol in `ABConnectTools` and zero rows with `status` unset.
- **SC-005** satisfied ⇔ every `ABConnect`-referencing line in `/src/lotsdb` produces exactly one `InventoryRow`.
- **SC-006** satisfied ⇔ every `GuideEntry` with a behavior change has a non-`none` `tiebreaker`.
