# Gap Recommendations — Prepare `ab` for Lotsdb Cutover

**Feature**: 036-lotsdb-migration-prep
**Date**: 2026-04-04
**Audience**: engineer executing the follow-up PR(s) against `ab` before the
Lotsdb cutover can ship.

Each section below is a standalone, implementable unit of work: what's
broken, what the target state looks like, the authoritative source to
match, and the minimum test to verify the fix. Sections are ordered by
**Lotsdb cutover impact**, highest first.

Tiebreaker order (per constitution §Sources of Truth): API server source
at `/src/ABConnect/` → captured fixtures → swagger (`ab/api/schemas/catalog.json`)
→ ABConnectTools (`/opt/pack/ABConnectTools/ABConnect/api/models/catalog.py`).
All four have been consulted for every recommendation below. For the
catalog/lot surface, swagger and ABConnectTools agree — the drift is
entirely on the `ab` side.

---

## Summary

| # | Gap | Severity | Affects | Type | Status |
|---|---|---|---|---|---|
| 1 | `BulkInsertRequest` model shape is wrong (flat `items: List[dict]` instead of nested catalogs) | **critical** | `importers.py`, every catalog import | correctness bug | **CLOSED** |
| 2 | `AddLotRequest` / `UpdateLotRequest` field set is wrong (7 wrong fields vs 5 real fields) | **critical** | `services.py`, `recovery.py`, `importers.py` | correctness bug | **CLOSED** |
| 3 | `AddCatalogRequest` / `UpdateCatalogRequest` field set is wrong (3 invented fields vs 6 real fields) | **critical** | any future Lotsdb catalog create/update | correctness bug | **CLOSED** |
| 4 | `LotDataDto` field set is missing 7 of 14 real fields | **critical** | all lot creates/updates lose data silently | correctness bug | **CLOSED** |
| 5 | `LotCatalogDto`, `LotCatalogInformationDto`, `BulkInsertCatalogRequest`, `BulkInsertLotRequest`, `BulkInsertSellerRequest`, `ImageLinkDto`, `SellerDto`, `CatalogDto` not present | **critical** | all of the above, plus `CatalogExpandedDto` response | missing models | **CLOSED** |
| 6 | `ABConnectAPI.login(username, password)` helper | **high** | Lotsdb form login (`services.py:22`) | missing helper | open |
| 7 | `FileLoader` replacement | **low** | Lotsdb `importers.py:250` only | rewrite on caller side | Lotsdb-side |

**Status update (branch `036-lotsdb-migration-prep`)**: Gaps 1–5
closed as a single rewrite. The implementation follows the
recommendation below — see `ab/api/models/{catalog,lots,sellers}.py`
on this branch. Verification:

- Every rewritten model's field aliases match
  `ab/api/schemas/catalog.json` exactly (scripted parity check, 16/16).
- A realistic nested `BulkInsertRequest` payload round-trips through
  the new models with mixed-case `LotDataDto` aliases (`Qty`, `L`,
  `W`, `H`, `Wgt`, `Cpack`, `ItemID`) serializing per swagger.
- `RequestModel.extra="forbid"` rejects typos at call time.
- Full pytest suite: 573 passed, 56 skipped, 5 xfailed.

**Still pending**: the 5 request fixtures under
`tests/fixtures/requests/` (`AddLotRequest.json`, `UpdateLotRequest.json`,
`AddCatalogRequest.json`, `UpdateCatalogRequest.json`,
`BulkInsertRequest.json`) now carry the correct **structure** but
hold all-null values (and `1970-01-01T00:00:00Z` sentinels for
required datetime fields). They must be re-captured against staging
via `examples/{catalog,lots}.py` before the Lotsdb cutover is safe to
ship — this is a Phase C step, not a model-level fix.

---

## Gap 1–5 (single PR) — Port the catalog / lot model surface

### What is broken today

`ab/api/models/catalog.py` and `ab/api/models/lots.py` contain
placeholder models that do not match the real API. The fields were
apparently invented by a prior pass without consulting the swagger JSON
that already sits at `ab/api/schemas/catalog.json`. Every field listed
below has been verified against (a) swagger in-repo, (b) ABConnectTools
source, and (c) where possible, captured fixtures.

**Drift table** — `ab` current vs authoritative (swagger + ABConnectTools
agree on every row):

| Model | `ab` current | Authoritative | Impact |
|---|---|---|---|
| `catalog.BulkInsertRequest` | `catalog_id: int`, `items: List[dict]` | `catalogs: List[BulkInsertCatalogRequest]` | Every Lotsdb catalog import would POST the wrong shape. Server likely 400s. |
| `catalog.AddCatalogRequest` | `title`, `agent_id` (as `agentId`), `seller_ids` | `customerCatalogId`, `agent` (not `agentId`), `title`, `startDate` (required), `endDate` (required), `sellerIds` | Missing two required datetime fields; `agent` was aliased incorrectly. |
| `catalog.UpdateCatalogRequest` | same wrong 3 fields | same as `AddCatalogRequest` | same |
| `lots.AddLotRequest` | `catalog_id`, `lot_number`, `data: dict` | `customerItemId`, `imageLinks`, `overridenData: List[LotDataDto]`, `catalogs: List[LotCatalogDto]`, `initialData: LotDataDto` (required) | Every Lot create would drop the item payload and fail validation. |
| `lots.UpdateLotRequest` | `lot_number`, `data: dict` | `customerItemId`, `imageLinks`, `overridenData`, `catalogs` | same |
| `lots.LotDataDto` | 7 fields (`qty`, `l→length`, `w`, `h`, `wgt`, `value`, `description`) | 14 fields — adds `cpack`, `notes`, `item_id`, `force_crate`, `noted_conditions`, `do_not_tip`, `commodity_id` | Silent data loss on every lot read/write. |
| `catalog.CatalogExpandedDto` | `sellers: List[dict]`, `lots: List[dict]` | `sellers: List[SellerDto]`, `lots: List[LotCatalogInformationDto]` | Loses validation on the response. |

**Missing classes** (referenced by the above, not present in `ab`):

- `LotCatalogDto`, `LotCatalogInformationDto`, `ImageLinkDto`, `SellerDto`, `CatalogDto`
- `BulkInsertCatalogRequest`, `BulkInsertLotRequest`, `BulkInsertSellerRequest`

### Target state

Two files, fully rewritten to match swagger. Reference implementations
to read before writing: `/opt/pack/ABConnectTools/ABConnect/api/models/catalog.py`
lines 52–294 (covers every class listed). Key conventions to preserve
from the existing `ab` codebase:

- Inherit from `RequestModel` (body) / `ResponseModel` (response) in
  `ab.api.models.base`, not from `ABConnectBaseModel`.
- snake_case Python names with camelCase `alias=` matching JSON. For
  write paths where the API expects PascalCase (seen in `LotDataDto`),
  use `validation_alias=AliasChoices(...)` + `serialization_alias=...`
  exactly as ABConnectTools does — see below.
- `RequestModel` sets `extra="forbid"`. Required swagger fields become
  required Python fields (not `Optional`) per constitution Principle IX.
- Add Sphinx-friendly `Field(..., description="…")` on every field.

#### `ab/api/models/lots.py` — target module

```python
"""Lot models for the Catalog API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import AliasChoices, Field, field_validator

from ab.api.models.base import RequestModel, ResponseModel


class LotDataDto(ResponseModel):
    """Nested data payload within a lot.

    API read responses use camelCase; API writes expect PascalCase.
    validation_alias reads both; serialization_alias writes PascalCase.
    Ported from ABConnectTools/api/models/catalog.py §LotDataDto.
    """

    model_config = {"populate_by_name": True, "extra": "ignore"}

    qty: Optional[int] = Field(
        None, validation_alias=AliasChoices("Qty", "qty"), serialization_alias="Qty",
        description="Quantity",
    )
    length: Optional[float] = Field(
        None, validation_alias=AliasChoices("L", "l"), serialization_alias="L",
        description="Length",
    )
    width: Optional[float] = Field(
        None, validation_alias=AliasChoices("W", "w"), serialization_alias="W",
        description="Width",
    )
    height: Optional[float] = Field(
        None, validation_alias=AliasChoices("H", "h"), serialization_alias="H",
        description="Height",
    )
    weight: Optional[float] = Field(
        None, validation_alias=AliasChoices("Wgt", "wgt"), serialization_alias="Wgt",
        description="Weight",
    )
    value: Optional[float] = Field(
        None, validation_alias=AliasChoices("Value", "value"), serialization_alias="Value",
        description="Declared value",
    )
    cpack: Optional[str] = Field(
        None, validation_alias=AliasChoices("CPack", "Cpack", "cpack"),
        serialization_alias="CPack", description="Container pack ID",
    )
    description: Optional[str] = Field(
        None, validation_alias=AliasChoices("Description", "description"),
        serialization_alias="Description",
    )
    notes: Optional[str] = Field(
        None, validation_alias=AliasChoices("Notes", "notes"),
        serialization_alias="Notes",
    )
    item_id: Optional[int] = Field(
        None, validation_alias=AliasChoices("ItemID", "itemID"),
        serialization_alias="ItemID", description="Item ID",
    )
    force_crate: Optional[bool] = Field(
        None, validation_alias=AliasChoices("ForceCrate", "forceCrate"),
        serialization_alias="ForceCrate",
    )
    noted_conditions: Optional[str] = Field(
        None, validation_alias=AliasChoices("NotedConditions", "notedConditions"),
        serialization_alias="NotedConditions",
    )
    do_not_tip: Optional[bool] = Field(
        None, validation_alias=AliasChoices("DoNotTip", "doNotTip"),
        serialization_alias="DoNotTip",
    )
    commodity_id: Optional[int] = Field(
        None, validation_alias=AliasChoices("CommodityId", "commodityId"),
        serialization_alias="CommodityId", description="Commodity/HS code ID",
    )

    @field_validator("commodity_id", "item_id", "qty", mode="before")
    @classmethod
    def _empty_string_to_none(cls, v):
        return None if v == "" else v


class ImageLinkDto(ResponseModel):
    id: int = Field(..., description="Image ID")
    link: str = Field(..., description="Image URL")


class LotCatalogDto(ResponseModel):
    """Lot-to-catalog association — also used as a body fragment in AddLotRequest."""

    catalog_id: int = Field(..., alias="catalogId", description="Parent catalog ID")
    lot_number: str = Field(..., alias="lotNumber", description="Lot number within catalog")


class LotCatalogInformationDto(ResponseModel):
    """Basic lot information embedded in a catalog response."""

    id: int = Field(..., description="Lot ID")
    lot_number: str = Field(..., alias="lotNumber", description="Lot number")


class LotDto(ResponseModel):
    """Full lot — returned by POST /Lot and GET /Lot/{id}."""

    id: int = Field(..., description="Lot ID")
    customer_item_id: Optional[str] = Field(None, alias="customerItemId")
    initial_data: LotDataDto = Field(..., alias="initialData")
    overriden_data: List[LotDataDto] = Field(default_factory=list, alias="overridenData")
    catalogs: List[LotCatalogDto] = Field(default_factory=list)
    image_links: List[ImageLinkDto] = Field(default_factory=list, alias="imageLinks")


class LotOverrideDto(LotDataDto):
    """Lot override data keyed by customer item ID."""

    customer_item_id: str = Field(..., alias="customerItemId")


class AddLotRequest(RequestModel):
    """Body for POST /Lot. All fields except initial_data are optional per swagger."""

    customer_item_id: Optional[str] = Field(None, alias="customerItemId")
    image_links: List[str] = Field(default_factory=list, alias="imageLinks")
    overriden_data: List[LotDataDto] = Field(default_factory=list, alias="overridenData")
    catalogs: List[LotCatalogDto] = Field(default_factory=list)
    initial_data: LotDataDto = Field(..., alias="initialData", description="Required initial lot data")


class UpdateLotRequest(RequestModel):
    """Body for PUT /Lot/{id}."""

    customer_item_id: Optional[str] = Field(None, alias="customerItemId")
    image_links: List[str] = Field(default_factory=list, alias="imageLinks")
    overriden_data: List[LotDataDto] = Field(default_factory=list, alias="overridenData")
    catalogs: List[LotCatalogDto] = Field(default_factory=list)


class LotListParams(RequestModel):
    """Query params for GET /Lot. Leave as-is if the current version already passes
    tests/test_example_params.py — swagger parameter names match what's there today."""
    # … keep existing fields from ab/api/models/lots.py unchanged; they already match.
```

#### `ab/api/models/catalog.py` — target module (delta only)

Replace the current `BulkInsertRequest`, `AddCatalogRequest`,
`UpdateCatalogRequest`, and the `List[dict]` placeholders in
`CatalogExpandedDto` with the correct definitions. Keep `CatalogListParams`
as-is (its fields match swagger already).

```python
from datetime import datetime
from ab.api.models.lots import LotDataDto, LotCatalogInformationDto


class SellerDto(ResponseModel):
    id: int
    name: Optional[str] = None
    customer_display_id: int = Field(..., alias="customerDisplayId")
    is_active: bool = Field(..., alias="isActive")


class CatalogDto(ResponseModel):
    id: int
    customer_catalog_id: Optional[str] = Field(None, alias="customerCatalogId")
    agent: Optional[str] = None
    title: Optional[str] = None
    start_date: datetime = Field(..., alias="startDate")
    end_date: datetime = Field(..., alias="endDate")
    is_completed: bool = Field(..., alias="isCompleted")


class CatalogWithSellersDto(CatalogDto):
    sellers: List[SellerDto] = Field(default_factory=list)


class CatalogExpandedDto(CatalogDto):
    sellers: List[SellerDto] = Field(default_factory=list)
    lots: List[LotCatalogInformationDto] = Field(default_factory=list)


class AddCatalogRequest(RequestModel):
    customer_catalog_id: Optional[str] = Field(None, alias="customerCatalogId")
    agent: Optional[str] = None
    title: Optional[str] = None
    start_date: datetime = Field(..., alias="startDate")
    end_date: datetime = Field(..., alias="endDate")
    seller_ids: List[int] = Field(default_factory=list, alias="sellerIds")


class UpdateCatalogRequest(AddCatalogRequest):
    """Identical shape to AddCatalogRequest per swagger."""


class BulkInsertSellerRequest(RequestModel):
    name: Optional[str] = None
    customer_display_id: int = Field(..., alias="customerDisplayId")
    is_active: bool = Field(..., alias="isActive")


class BulkInsertLotRequest(RequestModel):
    customer_item_id: str = Field(..., alias="customerItemId")
    lot_number: str = Field(..., alias="lotNumber")
    image_links: List[str] = Field(default_factory=list, alias="imageLinks")
    initial_data: LotDataDto = Field(..., alias="initialData")
    overriden_data: List[LotDataDto] = Field(default_factory=list, alias="overridenData")


class BulkInsertCatalogRequest(RequestModel):
    customer_catalog_id: str = Field(..., alias="customerCatalogId")
    agent: str
    title: str
    start_date: datetime = Field(..., alias="startDate")
    end_date: datetime = Field(..., alias="endDate")
    lots: List[BulkInsertLotRequest] = Field(default_factory=list)
    sellers: List[BulkInsertSellerRequest] = Field(default_factory=list)


class BulkInsertRequest(RequestModel):
    """Body for POST /Bulk/insert. Per swagger: a single `catalogs` list."""

    catalogs: List[BulkInsertCatalogRequest] = Field(default_factory=list)
```

Note: `AddSellerRequest` / `UpdateSellerRequest` / `GetLotsOverridesQuery`
are also in the ABConnectTools surface. Port them at the same time if
sellers-endpoint parity matters — they are small.

### Endpoint changes that follow

- `ab/api/endpoints/catalog.py::bulk_insert` — signature stays
  (`data: BulkInsertRequest | dict`), but the expected dict shape changes.
  No code change.
- `ab/api/endpoints/lots.py::create` / `update` — docstrings currently
  describe the wrong fields (`"catalog_id, lot_number, and data"`).
  Update the docstrings to list the real fields.

### Fixtures to (re)capture

Once the models are correct, the following fixture files under
`tests/fixtures/requests/` will no longer round-trip and must be
re-captured or hand-rewritten to match the new shape. Any fixture
that was captured against the wrong model is unsafe:

- `AddLotRequest.json`
- `UpdateLotRequest.json`
- `AddCatalogRequest.json`
- `UpdateCatalogRequest.json`
- `BulkInsertRequest.json`

For each, the constitution-compliant capture path is:
1. Run the matching example under `examples/` (create if absent).
2. 200 response → store the body the example sent.
3. Validate it round-trips through the new model with `extra="forbid"`.

### Verification

```bash
# Model shape parity vs swagger
python -c "
import json, re
from ab.api.models.catalog import (
    BulkInsertRequest, BulkInsertCatalogRequest, BulkInsertLotRequest,
    BulkInsertSellerRequest, AddCatalogRequest, UpdateCatalogRequest,
    CatalogExpandedDto, SellerDto, CatalogDto,
)
from ab.api.models.lots import (
    AddLotRequest, UpdateLotRequest, LotDataDto, LotCatalogDto,
    LotCatalogInformationDto, LotDto, ImageLinkDto,
)
schemas = json.load(open('ab/api/schemas/catalog.json'))['components']['schemas']
for cls in [BulkInsertRequest, BulkInsertCatalogRequest, AddLotRequest, UpdateLotRequest,
            AddCatalogRequest, LotDataDto, LotCatalogDto]:
    swagger_props = set(schemas[cls.__name__]['properties'].keys())
    model_aliases = {f.alias or name for name, f in cls.model_fields.items()}
    missing = swagger_props - model_aliases
    extra = model_aliases - swagger_props
    assert not missing and not extra, f'{cls.__name__}: missing={missing} extra={extra}'
print('OK')
"

# Existing suite must stay green
pytest tests/test_example_params.py tests/swagger/test_coverage.py
pytest tests/models/  # round-trip tests pick up any fixture mismatch
```

---

## Gap 6 — `ABConnectAPI.login(username, password)` helper

### What is broken today

`ab.ABConnectAPI.__init__` only accepts `env`, `env_file`, `request`.
Credentials are read from `Settings.username` / `.password` on first
HTTP call (see `ab/http.py::_password_grant` line 65). There is no
supported path for a caller to supply credentials at runtime — which
is exactly what Lotsdb's login form needs in `catalog/services.py:20-33`.

Workarounds like mutating `os.environ` before construction are racy
in multi-worker WSGI servers and leak credentials into child
processes.

### Target state

Add an explicit login method to `ABConnectAPI` that mints a token from
user-supplied credentials and primes the bound `TokenStorage`. The
Django-`request=` path then continues to work unchanged — the token
lives in the session.

```python
# ab/client.py — add to class ABConnectAPI
def login(self, username: str, password: str) -> None:
    """Authenticate with explicit credentials and prime token storage.

    Mints a token against the identity server using the supplied
    credentials and stores it via the bound :class:`TokenStorage`
    (file-based or Django session, depending on construction).

    Raises:
        ab.AuthenticationError: credentials rejected by identity server.
    """
    # Delegate to a new helper on HttpClient — any surface works,
    # they share the same identity endpoint.
    self._acportal._password_grant_with(username=username, password=password)
```

```python
# ab/http.py — add to class HttpClient
def _password_grant_with(self, *, username: str, password: str) -> Token:
    """Password grant using caller-supplied credentials (bypasses Settings)."""
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": self._settings.client_id,
        "client_secret": self._settings.client_secret,
        "scope": "offline_access",
    }
    resp = requests.post(self._settings.identity_url, data=data, timeout=self._settings.timeout)
    if not resp.ok:
        raise AuthenticationError(
            f"Login failed for {username}: {resp.status_code} {resp.text}"
        )
    return self._store_token(resp.json())
```

### Lotsdb usage pattern (after this lands)

```python
# catalog/services.py — replaces the old ABConnectAPI(..., username=..., password=...) call
def login(request, username, password):
    api = ab.ABConnectAPI(request=request)
    api.login(username, password)      # raises AuthenticationError on bad creds
    request.session["abc_username"] = username
    # … Django user bridge unchanged
```

### Verification

- Unit test `tests/auth/test_login_helper.py`: mock
  `requests.post` returning a fake token JSON, assert `api.login(...)`
  stores it into a `SessionTokenStorage` backed by a fake request.
- Unit test that bad credentials (`requests.post` → 400) raise
  `ab.AuthenticationError`.
- Smoke test against staging with a known service account in
  `examples/auth_login.py`.

### Alternatives considered

1. **Document the env-override workaround**: mutate `os.environ`
   before constructing. Rejected — racy in multi-worker servers,
   leaks secrets to subprocesses.
2. **Reach into `Settings` post-construction**: `api._settings.username = …`.
   Rejected — uses a private attribute and bypasses the Pydantic
   validators on `Settings`.
3. **Return a new API instance from a module-level `ab.login(...)`**.
   Rejected — caller needs the Django `request` bound to the same
   instance for session-backed token storage.

---

## Gap 7 — `FileLoader` replacement

### What is broken today

`ab` does not ship a spreadsheet/JSON/CSV reader. ABConnectTools ships
`FileLoader` (168-line class wrapping `pandas` + `openpyxl` + `chardet`
+ `BeautifulSoup`). Lotsdb uses exactly one surface of it:

```python
# catalog/importers.py:250
data = FileLoader(path.as_posix()).data   # list[dict]
```

### Recommendation: leave on the Lotsdb side

Do **not** port `FileLoader` into `ab`. `ab` is an HTTP SDK; spreadsheet
parsing is out of its concern. Lotsdb should rewrite the single call
site using the libraries it already depends on.

**Replacement in Lotsdb** (to paste into `catalog/importers.py`):

```python
from pathlib import Path
import json
import pandas as pd


def _load_rows(path: Path) -> list[dict]:
    """Read a spreadsheet/JSON file into a list of row dicts.

    Supports .xlsx / .xls / .csv / .json — the same set ABConnectTools
    FileLoader supported for Lotsdb's importers.
    """
    ext = path.suffix.lower()
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(path, na_filter=False).fillna("").to_dict("records")
    if ext == ".csv":
        return pd.read_csv(path, na_filter=False, encoding_errors="replace").fillna("").to_dict("records")
    if ext == ".json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    raise ValueError(f"Unsupported file type: {ext}")

# replace the line: data = FileLoader(path.as_posix()).data
data = _load_rows(path)
```

Lotsdb already depends on `pandas`/`openpyxl` transitively via Django +
Excel export tooling. If it doesn't, add them to Lotsdb's `pyproject.toml`
— they are ~1 line of dep declaration, vs dragging `FileLoader` into
`ab` as dead weight for every other consumer.

### Alternatives considered

1. **Port `FileLoader` into `ab` as `ab.io.FileLoader`**. Rejected —
   `ab` is an HTTP SDK, and adding `pandas`/`openpyxl`/`chardet`/`bs4`
   as hard dependencies would roughly triple the install footprint
   for every consumer, only to serve one Lotsdb call site.
2. **Port `FileLoader` into `ab.contrib` as optional**. Rejected —
   adds a conditional-import pattern and a new subpackage for a 10-line
   replacement that trivially fits in Lotsdb.

---

## Recommended execution order

1. **PR-A: Catalog/lot model rewrite** (Gaps 1–5, single PR).
   - Rewrite `ab/api/models/lots.py` and `ab/api/models/catalog.py`.
   - Update endpoint docstrings in `ab/api/endpoints/{lots,catalog}.py`.
   - Re-capture the 5 listed request fixtures via examples.
   - Run `pytest tests/test_example_params.py tests/swagger/test_coverage.py tests/models/`.
   - Merge.

2. **PR-B: `ABConnectAPI.login()` helper** (Gap 6).
   - Add the method + test in isolation.
   - Merge.

3. **Lotsdb cutover PR** (separate repo).
   - Apply `specs/036-lotsdb-migration-prep/lotsdb-inventory.md` rewrites.
   - Replace `FileLoader` per Gap 7.
   - Swap login flow per Gap 6.
   - Import lot/catalog models from the new `ab.api.models.{lots,catalog}`
     locations (lots moved out of the `catalog` module).
   - Run Lotsdb suite end-to-end.

PR-A and PR-B are independent — they can be parallelized. The Lotsdb
cutover PR depends on both.

## What is NOT in scope for this spec

- Actually writing PR-A or PR-B in this branch. This spec delivers
  the recommendations; implementation is left to dedicated feature
  branches because Gap 1–5 touches response shapes of existing models
  and could regress other consumers, and should be reviewed as its
  own focused PR.
- Modifying `/src/lotsdb/`. The Lotsdb cutover is a Lotsdb-repo PR.
- Adding test-capture infrastructure beyond what already exists; the
  constitution Principle II capture loop (run the example, save the
  200 body) remains the only sanctioned path.
