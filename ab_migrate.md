# Migrating from ABConnectTools to `ab`

Authoritative migration guide for consumers of `ABConnectTools` (the
legacy `ABConnect` Python package at `/opt/pack/ABConnectTools/`) who
are cutting over to the new `ab` SDK. Written for the Lotsdb cutover
(feature 036) but applies to any downstream project.

Tiebreaker order used throughout: (1) API server source at
`/src/ABConnect/`, (2) captured fixtures under
`/opt/pack/ab/tests/fixtures/`, (3) swagger snapshots at
`/opt/pack/ABConnectTools/ABConnect/base/*.json`, (4) `ABConnectTools`
source as a final fallback.

## TL;DR

1. **Package rename**: `from ABConnect import …` → `from ab import …`.
2. **Exceptions cleaned up**: `LoginFailedError` and `NotLoggedInError` are gone — catch `ab.AuthenticationError`. `ABConnectError` no longer carries `.code`, `.details`, `.to_dict()`, `.no_traceback()`.
3. **`ABConnectAPI(...)` signature narrowed**: no more `username=` / `password=` kwargs. Credentials come from env; only `env`, `env_file`, and `request` are accepted.
4. **Model module moves**: lot-related models moved from `ABConnect.api.models.catalog` to `ab.api.models.lots`. Some catalog bulk-insert models and `LotCatalogDto` are **not ported** — see [Known gaps](#gaps).
5. **Top-level helpers removed**: `FileLoader`, `APIRequestBuilder`, `Quoter`, and the `ABConnect.models` / `ABConnect.routes` runtime aliases are gone. No replacement — callers must rewrite.

## Version and dependency

- Minimum `ab` version: pin to whatever commit on `main` contains this file (or the first tagged release that does).
- Replacement dependency in `pyproject.toml`:

  ```toml
  # before
  dependencies = [
      "ABConnect @ file:///opt/pack/ABConnectTools",
  ]

  # after
  dependencies = [
      "ab @ file:///opt/pack/ab",
  ]
  ```

- After cutover, uninstall `ABConnectTools` from the target environment
  to prevent accidental `ABConnect.*` imports from resolving.

## Package rename

Every `ABConnect.*` import path is replaced with an `ab.*` path. The
runtime aliases `ABConnect.models` and `ABConnect.routes` do not exist
in `ab` — import models from their real module.

| ABConnectTools | `ab` |
|---|---|
| `from ABConnect import ABConnectAPI` | `from ab import ABConnectAPI` |
| `from ABConnect.exceptions import ABConnectError` | `from ab import ABConnectError` |
| `from ABConnect.exceptions import RequestError` | `from ab import RequestError` |
| `from ABConnect.exceptions import LoginFailedError` | _removed — catch `ab.AuthenticationError`_ |
| `from ABConnect.exceptions import NotLoggedInError` | _removed — catch `ab.AuthenticationError`_ |
| `from ABConnect import FileLoader` | _removed — rewrite caller, see [Removed helpers](#removed-helpers)_ |
| `from ABConnect import APIRequestBuilder` | _removed_ |
| `from ABConnect import Quoter` | _removed_ |
| `from ABConnect.api.models.catalog import AddLotRequest` | `from ab.api.models.lots import AddLotRequest` |
| `from ABConnect.api.models.catalog import UpdateLotRequest` | `from ab.api.models.lots import UpdateLotRequest` |
| `from ABConnect.api.models.catalog import LotDataDto` | `from ab.api.models.lots import LotDataDto` |
| `from ABConnect.api.models.catalog import LotCatalogDto` | _not ported — see [Known gaps](#gaps)_ |
| `from ABConnect.api.models.catalog import BulkInsertRequest` | `from ab.api.models.catalog import BulkInsertRequest` — **shape differs, see below** |
| `from ABConnect.api.models.catalog import BulkInsertCatalogRequest` | _not ported — see [Known gaps](#gaps)_ |
| `from ABConnect.api.models.catalog import BulkInsertSellerRequest` | _not ported — see [Known gaps](#gaps)_ |
| `from ABConnect.api.models.catalog import BulkInsertLotRequest` | _not ported — see [Known gaps](#gaps)_ |
| `from ABConnect.models import <X>` (runtime alias) | replace with the real module, e.g. `from ab.api.models.<module> import <X>` |
| `from ABConnect.routes import <X>` (runtime alias) | _removed — routes are private to endpoint modules in `ab`_ |

## Removed helpers

### `FileLoader`

**Status**: removed, no replacement.

`FileLoader` was a spreadsheet/JSON loader used by `ABConnectTools`
examples (e.g. `examples/catalog.py`). `ab` does not ship a file
loader — it is a pure HTTP SDK.

**Before**:

```python
from ABConnect import FileLoader

loader = FileLoader("catalog.xlsx")
rows = loader.rows()
```

**After**: use `openpyxl`, `pandas`, or the stdlib `csv`/`json` modules
directly in the caller.

```python
import pandas as pd
rows = pd.read_excel("catalog.xlsx").to_dict("records")
```

### `APIRequestBuilder`, `Quoter`

**Status**: removed, no replacement.

These were convenience wrappers that pre-date the typed endpoint
classes. Every request is now expressed via a typed endpoint method
on `ABConnectAPI` (e.g. `api.jobs.create(data=JobCreateRequest(...))`).

### `ABConnect.models` / `ABConnect.routes` runtime aliases

**Status**: removed.

`ABConnectTools/__init__.py` registered runtime aliases via
`sys.modules['ABConnect.models']` so you could write
`from ABConnect.models import X`. `ab` does not do this — import from
the real module path (`ab.api.models.<module>`).

## Exceptions

### Class map

| ABConnectTools | `ab` |
|---|---|
| `ABConnectError` | `ab.ABConnectError` (attribute shape changed, see below) |
| `RequestError` | `ab.RequestError` (constructor signature narrowed) |
| `LoginFailedError` | **removed** — catch `ab.AuthenticationError` |
| `NotLoggedInError` | **removed** — catch `ab.AuthenticationError` |

`ab` adds two new classes that do not exist in `ABConnectTools`:
`ab.AuthenticationError` (any auth failure — login, refresh, missing
token) and `ab.ConfigurationError` (bad env file, missing required
setting) and `ab.ValidationError` (non-Pydantic validation failures).

### Exception shape — silent regression

`ABConnectTools`'s `ABConnectError` carried extra attributes:

```python
# ABConnectTools
class ABConnectError(Exception):
    def __init__(self, message, *, code=None, details=None): ...
    def to_dict(self): ...
    def no_traceback(self): ...
    # .code, .details attributes
```

`ab`'s `ABConnectError` is a plain `Exception` subclass. No `.code`,
no `.details`, no `.to_dict()`, no `.no_traceback()`. **Imports will
still resolve** — any `except ABConnectError` block continues to
catch. But attribute access will `AttributeError` at runtime.

**Silently wrong patterns** that must be rewritten:

```python
# ABConnectTools — works
try:
    api.jobs.get(123)
except ABConnectError as e:
    logger.error(e.to_dict())          # ← breaks on ab
    logger.error("code=%s", e.code)    # ← breaks on ab
    logger.error(e.details.get("x"))   # ← breaks on ab
```

**Replacement**: log `str(e)` and the class name; inspect
`RequestError.status_code` specifically if you were reaching into
`.details["status_code"]`.

```python
# ab
try:
    api.jobs.get(123)
except ab.RequestError as e:
    logger.error("HTTP %s: %s", e.status_code, e.message)
except ab.AuthenticationError as e:
    logger.warning("Auth failed: %s", e)
except ab.ABConnectError as e:
    logger.error("ABConnect error: %s", e)
```

### `RequestError` constructor change

```python
# ABConnectTools
raise RequestError(status_code, message, response, code="X")

# ab — no response kwarg, no code kwarg
raise ab.RequestError(status_code, message)
```

`ab.RequestError` exposes `.status_code` and `.message`. There is no
`.response` attribute — if you previously inspected the response body
via `e.response.text`, you must capture it before raising.

### `LoginFailedError` / `NotLoggedInError`

Both classes are removed. `ab` raises `AuthenticationError` in both
situations (bad credentials, missing/expired token).

```python
# ABConnectTools
try:
    ABConnectAPI(request=request, username=u, password=p)
except LoginFailedError:
    show_bad_credentials_page()

# ab — both the constructor and the exception change
try:
    api = ab.ABConnectAPI(request=request)   # credentials come from env
    api.companies.available_by_current_user()  # force a token request to validate
except ab.AuthenticationError:
    show_bad_credentials_page()
```

Note: the *semantics* also change. On `ABConnectTools`, passing wrong
credentials into `ABConnectAPI(...)` raised at construction. On `ab`,
the constructor is purely local — network activity happens on first
request, so the exception surfaces from the first call, not the
constructor. Adjust any test that expected the constructor to raise.

## `ABConnectAPI` constructor

Signature changed:

```python
# ABConnectTools — accepted credentials inline
ABConnectAPI(request=request, username=username, password=password)
ABConnectAPI()                          # read from env
ABConnectAPI(env_file=".env.staging")

# ab — credentials never pass through the constructor
ab.ABConnectAPI(env="staging")
ab.ABConnectAPI(env_file=".env.staging")
ab.ABConnectAPI(request=django_request)
```

Only `env`, `env_file`, and `request` are accepted (all keyword-only).
Credentials are loaded from the env file and validated lazily on
first HTTP call. If you pass a Django `request`, the token is stored
in and read from `request.session["ab_token"]`.

**Lotsdb-specific**: `catalog/services.py::login(request, username, password)`
passed user-entered credentials directly to the constructor. There is
**no direct replacement** — `ab` only supports credentials sourced from
environment variables. Options:

1. **Service account (recommended)**: drop per-user credentials entirely and
   configure a single service account in the Django app's env file.
   `ABConnectAPI(request=request)` then mints a token for that service
   account and stores it in the session on first call.
2. **Temporarily override env**: before calling `ABConnectAPI(...)`,
   monkey-set `os.environ["AB_USERNAME"]` / `AB_PASSWORD` to the submitted
   values, then revert after the first HTTP call. Not recommended in
   multi-worker servers — racy.

Either choice is an architectural decision for Lotsdb, not a mechanical
rewrite. Tracked under [Known gaps](#gaps).

## Model relocations

| Symbol | Old location | New location |
|---|---|---|
| `AddLotRequest` | `ABConnect.api.models.catalog` | `ab.api.models.lots` |
| `UpdateLotRequest` | `ABConnect.api.models.catalog` | `ab.api.models.lots` |
| `LotDataDto` | `ABConnect.api.models.catalog` | `ab.api.models.lots` |
| `LotDto` | `ABConnect.api.models.catalog` | `ab.api.models.lots` |
| `LotOverrideDto` | `ABConnect.api.models.catalog` | `ab.api.models.lots` |
| `LotListParams` | `ABConnect.api.models.catalog` | `ab.api.models.lots` |
| `CatalogExpandedDto` | `ABConnect.api.models.catalog` | `ab.api.models.catalog` |
| `AddCatalogRequest` | `ABConnect.api.models.catalog` | `ab.api.models.catalog` |
| `UpdateCatalogRequest` | `ABConnect.api.models.catalog` | `ab.api.models.catalog` |
| `CatalogListParams` | `ABConnect.api.models.catalog` | `ab.api.models.catalog` |
| `BulkInsertRequest` | `ABConnect.api.models.catalog` | `ab.api.models.catalog` — **simplified; see [Known gaps](#gaps)** |
| `BulkInsertCatalogRequest` | `ABConnect.api.models.catalog` | **not ported** |
| `BulkInsertSellerRequest` | `ABConnect.api.models.catalog` | **not ported** |
| `BulkInsertLotRequest` | `ABConnect.api.models.catalog` | **not ported** |
| `LotCatalogDto` | `ABConnect.api.models.catalog` | **not ported** |
| `LotCatalogInformationDto` | `ABConnect.api.models.catalog` | **not ported** |

### `RequestModel` validation (new behavior)

`ab` request models inherit from `RequestModel` which sets
`extra="forbid"`. If you previously passed dicts with extra keys, they
would silently succeed; under `ab` they now raise `ValidationError` at
call time. This is intentional — it catches typos before the HTTP
request.

## Endpoint parity

`ab` has the full endpoint surface Lotsdb needs: `api.catalog`,
`api.lots`, `api.sellers`, `api.companies` (28 methods), `api.jobs`
(59 methods). All endpoint methods make real HTTP calls via the
shared client.

However, several **model shapes** on the catalog/lot surface in `ab`
are currently wrong — they do not match swagger or the real server
contract. A Lotsdb cutover using these models today would fail
validation or POST the wrong shape. See
[`specs/036-lotsdb-migration-prep/gap-recommendations.md`](specs/036-lotsdb-migration-prep/gap-recommendations.md)
for the complete drift table and implementation recommendations.

Gap status before the Lotsdb cutover:

| # | Gap | Severity | Status |
|---|---|---|---|
| 1 | `BulkInsertRequest` model shape (flat → nested catalogs) | critical | **closed** in this branch — see `ab/api/models/catalog.py::BulkInsertRequest` |
| 2 | `AddLotRequest` / `UpdateLotRequest` field set | critical | **closed** — see `ab/api/models/lots.py` |
| 3 | `AddCatalogRequest` / `UpdateCatalogRequest` field set | critical | **closed** — see `ab/api/models/catalog.py` |
| 4 | `LotDataDto` field set (7 → 14 fields, mixed casing) | critical | **closed** — see `ab/api/models/lots.py::LotDataDto` |
| 5 | Missing classes: `LotCatalogDto`, `LotCatalogInformationDto`, `BulkInsertCatalogRequest`, `BulkInsertLotRequest`, `BulkInsertSellerRequest`, `ImageLinkDto`, `SellerDto` (fixed), `CatalogDto` (added) | critical | **closed** |
| 6 | `ABConnectAPI.login(username, password)` helper | high | **open** — follow-up PR, see [gap-recommendations.md §Gap 6](specs/036-lotsdb-migration-prep/gap-recommendations.md#gap-6--abconnectapiloginusername-password-helper) |
| 7 | `FileLoader` replacement | low | **Lotsdb-side rewrite** — ~15 lines of pandas/json, see [Gap 7](specs/036-lotsdb-migration-prep/gap-recommendations.md#gap-7--fileloader-replacement) |

Gaps 1–5 are closed on branch `036-lotsdb-migration-prep`. Every model
field alias now matches `ab/api/schemas/catalog.json` exactly (verified
programmatically), and a realistic nested `BulkInsertRequest` payload
round-trips through the model layer with mixed-case `LotDataDto`
serialization (`Qty`, `L`, `W`, `H`, `Wgt`, `Cpack`, `ItemID`).
`extra="forbid"` on `RequestModel` catches typos at call time.

Gap 6 (login helper) is still open — it's an independent small PR in
a follow-up branch. Gap 7 is a Lotsdb-side rewrite.

## Tiebreaker log

During the preparation for this migration, every conflict between
`ab` and the real API was resolved in favour of the authoritative
source. The resolutions are recorded here.

| # | Discrepancy | Tiebreaker used | Decision |
|---|---|---|---|
| 1 | `ab.api.models.catalog.BulkInsertRequest` had `catalog_id` + `items: List[dict]` vs swagger `catalogs: List[BulkInsertCatalogRequest]` | swagger (`ab/api/schemas/catalog.json:1835`) + ABConnectTools agree | Rewrite per swagger. See [gap-recommendations.md](specs/036-lotsdb-migration-prep/gap-recommendations.md) Gap 1. |
| 2 | `ab.api.models.lots.{Add,Update}LotRequest` had `catalog_id`/`lot_number`/`data` vs swagger `customerItemId`/`imageLinks`/`overridenData`/`catalogs`/`initialData` | swagger + ABConnectTools agree | Rewrite per swagger. Gap 2. |
| 3 | `ab.api.models.catalog.{Add,Update}CatalogRequest` had `title`/`agent_id`/`seller_ids` vs swagger `customerCatalogId`/`agent`/`title`/`startDate`/`endDate`/`sellerIds` | swagger + ABConnectTools agree | Rewrite per swagger. Gap 3. |
| 4 | `ab.api.models.lots.LotDataDto` had 7 fields; ABConnectTools + server DTO have 14 | server DTO (`/src/ABConnect/ABConnect.Catalog*`) + ABConnectTools | Add the 7 missing fields: `cpack`, `notes`, `item_id`, `force_crate`, `noted_conditions`, `do_not_tip`, `commodity_id`. Gap 4. |

## Cutover checklist

Ordered steps for the Lotsdb cutover PR. Tick them off in order:

1. [ ] Add `ab` to the Lotsdb dependency file; remove `ABConnectTools`.
2. [ ] Configure `AB_USERNAME` / `AB_PASSWORD` / `AB_ENVIRONMENT` in the Lotsdb env file using a dedicated service account (see [Constructor](#abconnectapi-constructor)).
3. [ ] Run `grep -rn "ABConnect" src/ pyproject.toml` — every hit must land in `specs/036-lotsdb-migration-prep/lotsdb-inventory.md`.
4. [ ] For each inventory row with `action == rewrite`, apply the rewrite mechanically.
5. [ ] Rewrite `catalog/services.login` per [Constructor](#abconnectapi-constructor). This is **not mechanical** — see [Known gaps](#gaps).
6. [ ] Rewrite `catalog/importers.py` to drop `FileLoader` and the missing `BulkInsert*` models — see [Known gaps](#gaps).
7. [ ] Rewrite any `except ABConnectError as e: …e.code…` / `e.details` / `e.to_dict()` pattern to log `str(e)` + `type(e).__name__`.
8. [ ] Replace `except LoginFailedError` / `except NotLoggedInError` with `except ab.AuthenticationError`.
9. [ ] Run `python -c "from ab import ABConnectAPI; print(ABConnectAPI)"` in the Lotsdb venv to confirm the SDK resolves.
10. [ ] Run the Lotsdb test suite. Fix any regressions.
11. [ ] Smoke-test the login flow manually against staging.
12. [ ] Smoke-test catalog import manually — the most invasive rewrite.
13. [ ] Uninstall `ABConnectTools` from the venv and confirm no lingering imports resolve.

## Known gaps

Status as of branch `036-lotsdb-migration-prep`:

1. **Catalog/lot model surface** (Gap 1–5) — **CLOSED** on this
   branch. Every `ab.api.models.{catalog,lots,sellers}` class that
   Lotsdb touches now matches `ab/api/schemas/catalog.json` field for
   field. `BulkInsertRequest` is nested; `LotDataDto` carries all 14
   fields with mixed-case aliases per swagger; `LotCatalogDto`,
   `LotCatalogInformationDto`, `BulkInsertCatalogRequest`,
   `BulkInsertLotRequest`, `BulkInsertSellerRequest`, `ImageLinkDto`,
   `CatalogDto` are new; `SellerDto` was fixed. See [gap-recommendations.md Gap 1–5](specs/036-lotsdb-migration-prep/gap-recommendations.md#gap-15-single-pr--port-the-catalog--lot-model-surface)
   for the drift table that drove the rewrite. Fixture re-capture
   against staging is still pending — request fixtures under
   `tests/fixtures/requests/` hold structural placeholders with
   `1970-01-01T00:00:00Z` sentinels for required datetime fields;
   values must be replaced via real captures before the Lotsdb
   cutover ships.

2. **Credential-based login path** — **OPEN**. `ab.ABConnectAPI(...)`
   does not accept `username=`/`password=`, and there is no helper
   method to prime the bound `TokenStorage` from form-submitted
   credentials. **Action**: add `ABConnectAPI.login(username, password)`
   per [Gap 6 in the recommendations doc](specs/036-lotsdb-migration-prep/gap-recommendations.md#gap-6--abconnectapiloginusername-password-helper).
   Small, independent follow-up PR. Lotsdb's `catalog/services.py:22`
   remains blocked until this lands.

3. **`FileLoader` replacement** — **Lotsdb-side rewrite**, not an `ab`
   gap. `ab` is an HTTP SDK and should not take on `pandas`/`openpyxl`/
   `chardet`/`bs4` dependencies for one caller. Lotsdb can replace the
   single `FileLoader(path).data` call site with ~15 lines using
   libraries it already depends on. See [Gap 7 in the recommendations doc](specs/036-lotsdb-migration-prep/gap-recommendations.md#gap-7--fileloader-replacement).

4. **`ABConnectError.code` / `.details` / `.to_dict()` access —
   silent regression**. `except ABConnectError` still compiles but
   attribute access fails at runtime. Not a gap in `ab` — the
   exception cleanup is intentional. **Action** for the Lotsdb PR:
   grep for `.to_dict()`, `.code`, `.details` inside any `except`
   block and rewrite to use `str(e)` + `type(e).__name__`.
