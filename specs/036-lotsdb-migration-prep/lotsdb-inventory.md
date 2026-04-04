# Lotsdb Call-Site Inventory

**Feature**: 036-lotsdb-migration-prep
**Generated**: 2026-04-04
**Regenerate with**:

```bash
grep -rn "ABConnect" /src/lotsdb/src /src/lotsdb/pyproject.toml
```

Every row below maps to an anchor in [`ab_migrate.md`](../../ab_migrate.md).
Apply `rewrite` rows mechanically; `block` rows require a human
decision per the guide's [Known gaps](../../ab_migrate.md#known-gaps).

## Totals

| Total | Rewrite | Remove | Block | No-change |
|---:|---:|---:|---:|---:|
| 28 | 12 | 0 | 2 | 14 |

**Block rows surfaced first** — after Gaps 1–5 were closed on this
branch, only two blockers remain:

- `services.py:22` — `ABConnectAPI(request=..., username=..., password=...)`: still **block**, waits on Gap 6 (`ABConnectAPI.login()` helper). After that follow-up PR lands, rewrite to `api = ab.ABConnectAPI(request=request); api.login(username, password)`.
- `importers.py:11` — `from ABConnect import FileLoader`: **Lotsdb-side rewrite** using pandas/openpyxl. See [Gap 7](./gap-recommendations.md#gap-7--fileloader-replacement) for a drop-in replacement.

**Previously blocked, now unblocked by Gaps 1–5 closure on this branch**:

- `services.py:199` — imports `UpdateLotRequest`, `LotDataDto`: model field sets are now correct; rewrite the import path to `ab.api.models.lots`.
- `services.py:334` — imports `LotCatalogDto`: now present in `ab.api.models.lots`; rewrite the import path.
- `importers.py:12` — imports `BulkInsertCatalogRequest`, `BulkInsertSellerRequest`, `BulkInsertLotRequest`, `BulkInsertRequest`: all four now exported from `ab.api.models.catalog`; rewrite the import path. Note that the shapes differ from the old ABConnectTools versions — the `CatalogDataBuilder` in `importers.py` produces the right nested structure, but re-verify field names (camelCase aliases) match the new models.

Before shipping the Lotsdb cutover, also re-capture the 5 request
fixtures under `ab/tests/fixtures/requests/` against staging via the
matching `ab/examples/{catalog,lots}.py` runs — see
[gap-recommendations.md](./gap-recommendations.md) "Still pending"
note in the Summary table.

---

## `src/catalog/services.py`

| Line | Category | Old | New | Action | Guide anchor | Tiebreaker | Notes |
|---|---|---|---|---|---|---|---|
| 6 | import | `from ABConnect import ABConnectAPI` | `from ab import ABConnectAPI` | rewrite | [#package-rename](../../ab_migrate.md#package-rename) | none | |
| 21 | string | `"""Authenticate via ABConnect, ..."""` | `"""Authenticate via ab, ..."""` | rewrite | [#package-rename](../../ab_migrate.md#package-rename) | none | docstring only |
| 22 | call | `ABConnectAPI(request=request, username=username, password=password)` | see notes | **block** | [#abconnectapi-constructor](../../ab_migrate.md#abconnectapi-constructor) | server | Constructor no longer accepts `username=` / `password=`. Switch to a service-account credential in the env file; form-supplied credentials are not supported by `ab` today. Item (4) in [Known gaps](../../ab_migrate.md#known-gaps). |
| 39 | string | `# ... only one ABConnectAPI (and one` | `# ... only one ABConnectAPI (and one` | rewrite | [#package-rename](../../ab_migrate.md#package-rename) | none | comment — leave name or update to `ab.ABConnectAPI` |
| 43 | call | `ABConnectAPI(request=request).catalog` | `ABConnectAPI(request=request).catalog` | no_change | [#abconnectapi-constructor](../../ab_migrate.md#abconnectapi-constructor) | server | `request=` kwarg is still supported; `.catalog` endpoint group still exists. Verify attribute name at cutover time — may be `.catalog` or another alias. |
| 199 | import | `from ABConnect.api.models.catalog import UpdateLotRequest, LotDataDto` | `from ab.api.models.lots import UpdateLotRequest, LotDataDto` | rewrite | [#model-relocations](../../ab_migrate.md#model-relocations) | swagger | Unblocked — Gap 1–5 closed on branch `036-lotsdb-migration-prep`. Note the `UpdateLotRequest` field set is now `customerItemId`/`imageLinks`/`overridenData`/`catalogs` — any construction of this request dict in Lotsdb must change accordingly. |
| 334 | import | `from ABConnect.api.models.catalog import AddLotRequest, LotDataDto, LotCatalogDto` | `from ab.api.models.lots import AddLotRequest, LotDataDto, LotCatalogDto` | rewrite | [#model-relocations](../../ab_migrate.md#model-relocations) | swagger | Unblocked — all three symbols now live in `ab.api.models.lots`. `AddLotRequest` shape changed: construction dicts must use `customerItemId`/`imageLinks`/`overridenData`/`catalogs`/`initialData` instead of `catalogId`/`lotNumber`/`data`. |

## `src/catalog/importers.py`

| Line | Category | Old | New | Action | Guide anchor | Tiebreaker | Notes |
|---|---|---|---|---|---|---|---|
| 3 | string | `# Adapted from ABConnectTools examples/catalog.py.` | `# Adapted from ABConnectTools examples/catalog.py (ported to ab).` | rewrite | [#package-rename](../../ab_migrate.md#package-rename) | none | comment |
| 11 | import | `from ABConnect import FileLoader` | _remove — rewrite caller_ | **block** | [#removed-helpers](../../ab_migrate.md#removed-helpers) | none | `FileLoader` is not ported; rewrite the import logic using `openpyxl` / `pandas` / stdlib `csv` / `json`. Item (1) in [Known gaps](../../ab_migrate.md#known-gaps). |
| 12 | import | `from ABConnect.api.models.catalog import ( BulkInsertRequest, BulkInsertCatalogRequest, BulkInsertSellerRequest, BulkInsertLotRequest, LotDataDto, )` | `from ab.api.models.catalog import BulkInsertRequest, BulkInsertCatalogRequest, BulkInsertSellerRequest, BulkInsertLotRequest` + `from ab.api.models.lots import LotDataDto` | rewrite | [#model-relocations](../../ab_migrate.md#model-relocations) | swagger | Unblocked — Gap 1–5 closed on branch `036-lotsdb-migration-prep`. All four `BulkInsert*` classes are now present in `ab.api.models.catalog` and match swagger. `BulkInsertRequest.catalogs` is a list of nested `BulkInsertCatalogRequest` with embedded `lots` + `sellers`. Re-verify the `CatalogDataBuilder` produces this nested shape. |

## `src/catalog/management/commands/import_catalog.py`

| Line | Category | Old | New | Action | Guide anchor | Tiebreaker | Notes |
|---|---|---|---|---|---|---|---|
| 7 | import | `from ABConnect import ABConnectAPI` | `from ab import ABConnectAPI` | rewrite | [#package-rename](../../ab_migrate.md#package-rename) | none | |
| 50 | call | `api = ABConnectAPI()` | `api = ABConnectAPI()` | no_change | [#abconnectapi-constructor](../../ab_migrate.md#abconnectapi-constructor) | server | No-arg constructor still supported — reads credentials from env file. |

## `src/catalog/views/auth.py`

| Line | Category | Old | New | Action | Guide anchor | Tiebreaker | Notes |
|---|---|---|---|---|---|---|---|
| 7 | import | `from ABConnect.exceptions import LoginFailedError, ABConnectError` | `from ab import AuthenticationError, ABConnectError` | rewrite | [#exceptions](../../ab_migrate.md#exceptions) | server | `LoginFailedError` removed; catch `AuthenticationError` instead. |
| 26 | type | `except LoginFailedError:` | `except AuthenticationError:` | rewrite | [#exceptions](../../ab_migrate.md#exceptions) | server | |
| 33 | type | `except (ABConnectError, Exception) as e:` | `except (ABConnectError, Exception) as e:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | Class still exists, but verify no attribute access on `e.code` / `e.details` / `e.to_dict()` inside the block. |

## `src/catalog/views/sellers.py`

| Line | Category | Old | New | Action | Guide anchor | Tiebreaker | Notes |
|---|---|---|---|---|---|---|---|
| 5 | import | `from ABConnect.exceptions import ABConnectError` | `from ab import ABConnectError` | rewrite | [#package-rename](../../ab_migrate.md#package-rename) | none | |
| 115 | type | `except ABConnectError:` | `except ABConnectError:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | No attributes accessed — safe. |
| 117 | type | `except ABConnectError:` | `except ABConnectError:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | No attributes accessed — safe. |

## `src/catalog/views/panels.py`

| Line | Category | Old | New | Action | Guide anchor | Tiebreaker | Notes |
|---|---|---|---|---|---|---|---|
| 8 | import | `from ABConnect.exceptions import ABConnectError` | `from ab import ABConnectError` | rewrite | [#package-rename](../../ab_migrate.md#package-rename) | none | |
| 123 | type | `except ABConnectError:` | `except ABConnectError:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | Re-verify at cutover time that no `.code` / `.details` / `.to_dict()` access occurs inside the block. |
| 181 | type | `except ABConnectError:` | `except ABConnectError:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | same |
| 194 | type | `except ABConnectError:` | `except ABConnectError:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | same |
| 263 | type | `except ABConnectError:` | `except ABConnectError:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | same |
| 341 | type | `except ABConnectError:` | `except ABConnectError:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | same |
| 366 | type | `except ABConnectError:` | `except ABConnectError:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | same |
| 449 | type | `except ABConnectError:` | `except ABConnectError:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | same |
| 504 | type | `except ABConnectError:` | `except ABConnectError:` | no_change | [#exceptions](../../ab_migrate.md#exceptions) | server | same |

## `src/catalog/views/recovery.py`

| Line | Category | Old | New | Action | Guide anchor | Tiebreaker | Notes |
|---|---|---|---|---|---|---|---|
| 1 | import | `from ABConnect.api.models.catalog import AddLotRequest` | `from ab.api.models.lots import AddLotRequest` | rewrite | [#model-relocations](../../ab_migrate.md#model-relocations) | server | |

## Files not in the grep but worth verifying at cutover time

- `pyproject.toml` / `requirements*.txt` — confirm the `ABConnect`/`ABConnectTools` dependency is replaced with `ab` and all lock files are regenerated. Not currently in the grep output because the name may not include the literal string `ABConnect`.
- `tests/` — re-run the grep with `tests/` included once; this inventory only covered `src/` and `pyproject.toml` per the task prompt.
- Template files (`*.html`) — unlikely but grep them once to be safe.
