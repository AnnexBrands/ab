# Phase 0 Research — Lotsdb Migration Prep

**Feature**: 036-lotsdb-migration-prep
**Date**: 2026-04-04

Purpose: resolve all "NEEDS CLARIFICATION" items implied by the Technical Context in `plan.md`, freeze baseline facts about the two packages, and lock in the tiebreaker sources the implementer will actually use.

## R1 — Tiebreaker source availability

**Decision**: Use this concrete lookup order on the current host:

1. **Tier 1 (server source)**: `/src/ABConnect/` — .NET controllers and DTOs under `ACPortal/`, `ABC.WebAPI/`, `AB.ABCEntities/`, `ABC.Services/`. Confirmed present.
2. **Tier 2 (captured fixtures)**: `/opt/pack/ab/tests/fixtures/` (63+ response files) and `/opt/pack/ab/tests/fixtures/requests/` (118 request files).
3. **Tier 3 (swagger snapshots)**: on-disk copies inside `ABConnectTools` — `ACPortal_swagger_latest.json`, `ACPortal_709_swagger.json`, `Catalog_709_swagger.json`, `swagger.json` at `/opt/pack/ABConnectTools/ABConnect/base/`. These are the canonical swagger references because no swagger JSON is checked into the `ab` repo.
4. **Tier 4 (ABConnectTools source)**: `/opt/pack/ABConnectTools/ABConnect/api/endpoints/` — used only as a final tiebreaker when Tiers 1–3 are silent, per user instruction.

**Rationale**: Constitution §Sources of Truth mandates server source → fixtures → swagger. User added `ABConnectTools` as an explicit tiebreaker; it slots in below swagger because swagger is at least auto-generated from the server while `ABConnectTools` reflects historical decisions that may have drifted.

**Alternatives considered**:
- Fetching swagger over the network from staging URLs (per constitution §API Coverage table). Rejected: audit must run deterministically in CI without network or credentials, and on-disk snapshots exist.
- Treating `ABConnectTools` as Tier 2 ("legacy-validated fixture equivalent"). Rejected: ABConnectTools is a consumer, not a source of truth, and the constitution does not grant it authority.

## R2 — Baseline `ABConnectTools` public surface to enumerate in the guide

**Decision**: Enumerate at minimum:

- **Top-level package exports** (`ABConnect/__init__.py`): `FileLoader`, `APIRequestBuilder`, `Quoter`, `ABConnectAPI`, the `models` alias, the `routes` alias. Version constants (`__version__`, `VERSION`).
- **Exceptions** (`ABConnect/exceptions.py`): `ABConnectError`, `RequestError`, `NotLoggedInError`, `LoginFailedError` — and the attribute shape (`code`, `details`, `to_dict()`, `no_traceback()`, `response`).
- **Endpoint modules** (`ABConnect/api/endpoints/*.py`): `account`, `address`, `admin`, `commoditymap`, `commodity`, `companies`, `company`, `contacts`, `dashboard`, `documents`, `email`, `e_sign`, `jobintacct`, `jobs/*`, `lookup`, `note`, `notifications`, `partner`, `reports`, `rfq`, `shipment`, `SmsTemplate`, `users`, `v2`, `v3`, `Values`, `views`, `webhooks`.
- **Models namespace**: the runtime alias `sys.modules['ABConnect.models']` that exposes every `ABConnect/api/models/*.py` under a shortened path. Every symbol Lotsdb imports from `ABConnect.api.models.catalog` must be mapped to its new location.

**Rationale**: Each of these categories is either used by Lotsdb today (confirmed via grep) or is a plausible source of hidden drift once Lotsdb rewrites catch.

**Alternatives considered**: Only documenting symbols Lotsdb currently imports. Rejected — the guide must also protect against near-term Lotsdb additions and other consumers that copy lotsdb as a template.

## R3 — Baseline `ab` public surface

**Decision**: The authoritative `ab` exports are those declared in `/opt/pack/ab/ab/__init__.py` (`ABConnectAPI`, `ABConnectError`, `AuthenticationError`, `ConfigurationError`, `RequestError`, `ValidationError`) plus endpoint groups exposed on `ABConnectAPI` instances and models under `ab/api/models/`.

**Key deltas already confirmed** (feed directly into `ab_migrate.md`):

| Area | ABConnectTools | `ab` | Break type |
|---|---|---|---|
| Import root | `from ABConnect import …` | `from ab import …` | Rename |
| Top-level helpers | `FileLoader`, `APIRequestBuilder`, `Quoter` | not exported | Removed |
| Model alias | `ABConnect.models.*` | — | Removed |
| Route alias | `ABConnect.routes.*` | — | Removed |
| Exception: `NotLoggedInError` | present | absent | Removed (catch `AuthenticationError`) |
| Exception: `LoginFailedError` | present | absent | Removed (catch `AuthenticationError`) |
| `ABConnectError` attrs | `code`, `details`, `to_dict()`, `no_traceback()` | plain `Exception` subclass | Silent regression — import resolves, attributes don't exist |
| `RequestError` constructor | `RequestError(status_code, message, response, *, code=...)` | `RequestError(status_code, message)` | Signature change |
| `ABConnectAPI.__init__` | accepts `username=`, `password=` (Lotsdb uses this) | `env`, `env_file`, `request` only | Signature narrowed |
| Lot models | `ABConnect.api.models.catalog.{AddLotRequest, UpdateLotRequest, LotDataDto, LotCatalogDto}` | `ab.api.models.lots.{AddLotRequest, UpdateLotRequest, LotDataDto}` — `LotCatalogDto` not found | Module move + one symbol unported |

**Rationale**: Every entry here is a confirmed Lotsdb break site (see R5) or a confirmed export difference (see R2). No speculative entries.

## R4 — Endpoint inventory in `ab` and stub risk

**Decision**: The audit enumerates 25 endpoint modules under `ab/api/endpoints/` (excluding `__init__.py`). Method counts by module (from `grep -c "def "`):

```
address 2, autoprice 2, catalog 6, commodities 5, commodity_maps 5,
companies 28, contacts 12, dashboard 9, documents 4, forms 22,
jobs 59, lookup 16, lots 6, notes 4, partners 3, payments 10,
reports 8, rfq 7, sellers 5, shipments 16, users 4, views 8, web2lead 2
```

Total ≈ 243 `def` declarations (includes helpers and `__init__`). Audit must filter to public endpoint-method signatures (name not starting with `_`, class method on an `Endpoint` subclass, references `self._client`/`self._post`/etc.).

**Stub scan**: `grep -n "NotImplementedError"` across `ab/api/endpoints/` returns zero hits. Good baseline — FR-006 should be provably satisfied by a static check rather than a manual walk.

**Audit approach (decided)**: use `ast` to parse each endpoint module, collect method definitions, walk bodies looking for:

1. A call against the instance HTTP client (`self._client.get/post/put/patch/delete` or equivalent wrapper / `@route` decorator invocation).
2. Presence of a route decoration or inline path string.
3. Reference to a body model (arg typed as a `RequestModel` subclass, or a dict validated against one).

Any method failing (1) is a stub candidate; any method with a body-typed arg lacking a matching fixture under `tests/fixtures/requests/` is a fixture gap.

**Rationale**: Deterministic, no network, runs in under a second. Matches Principle IX's automated-enforcement style (`tests/test_example_params.py`).

**Alternatives considered**: Runtime introspection by importing `ABConnectAPI` and poking attributes. Rejected — pulls in real auth/config and slows CI.

## R5 — Lotsdb call-site reference set (frozen at spec time)

**Decision**: The following files in `/src/lotsdb` reference `ABConnect` today (fresh grep at spec time):

```
src/catalog/services.py
src/catalog/importers.py
src/catalog/management/commands/import_catalog.py
src/catalog/views/auth.py
src/catalog/views/sellers.py
src/catalog/views/panels.py
src/catalog/views/recovery.py
```

Known imports observed:

- `from ABConnect import ABConnectAPI` — `services.py`, `import_catalog.py`.
- `from ABConnect import FileLoader` — `importers.py`.
- `from ABConnect.api.models.catalog import {AddLotRequest, UpdateLotRequest, LotDataDto, LotCatalogDto, ...}` — `importers.py`, `services.py`, `recovery.py`.
- `from ABConnect.exceptions import ABConnectError` — `sellers.py`, `panels.py`.
- `from ABConnect.exceptions import LoginFailedError, ABConnectError` — `auth.py`.
- Call site: `ABConnectAPI(request=request, username=username, password=password)` — `services.py`.
- Call site: `ABConnectAPI(request=request)` — `services.py` (cached path), `import_catalog.py` (no args).

The inventory MUST be regenerated at execution time (a fresh grep may add files); this set is the documented baseline.

**Rationale**: Fresh data; keeps the plan honest about what is actually broken.

## R6 — Fixture category taxonomy

**Decision**: Three fixture categories the audit tracks per endpoint method:

1. **Path params** — path-bound values that substitute into the route template (e.g. `{companyId}`). Represented by a realistic value cached in a fixture file or in a known `tests/fixtures/ids.json`-style registry. If the method takes only path params, "query" and "body" are recorded as `N/A`.
2. **Query params** — values passed via `params=` to the HTTP client. Stored under `tests/fixtures/requests/{ParamsModelName}.json` or matched against a `RequestModel` subclass suffixed `Params`.
3. **Request body** — JSON sent via `json=`. Stored under `tests/fixtures/requests/{RequestModelName}.json` and must round-trip through the model with `extra="forbid"`.

**Existing inventory**: 118 files in `tests/fixtures/requests/`. The audit joins endpoint method signatures against this directory by class name.

**Rationale**: Matches existing fixture layout in `ab`; requires no migration of files.

## R7 — Authentication flow replacement

**Decision**: The guide will document that `ABConnectAPI` in `ab` obtains credentials via environment (`load_settings(env, env_file)`) or a Django request session (`request=`), and no longer accepts `username` / `password` as keyword arguments. Lotsdb call sites that currently pass credentials must either:

- Set the credentials in the env file the site already loads at startup, and drop the kwargs; or
- Mint a short-lived session using a documented helper exposed on `ab.auth`.

**Rationale**: Matches the constructor evidence in `ab/client.py`. The guide explicitly names the dropped kwargs so a grep surfaces every caller.

## R8 — Deliverable locations

**Decision**:

- `ab_migrate.md` → repo root (alongside `FIXTURES.md`, `README.md`).
- `scripts/audit_lotsdb_migration.py` → `scripts/` (matches existing tooling).
- `tests/test_migration_audit.py` → runs the audit script as a unit test; fails on regressions.
- `specs/036-lotsdb-migration-prep/audit.md` → checked-in snapshot of the most recent audit output.
- `specs/036-lotsdb-migration-prep/lotsdb-inventory.md` → call-site inventory.

**Rationale**: Keeps user-facing doc at repo root where consumers expect it; keeps feature-specific analysis under the feature directory.

## R9 — What is NOT researched (deferred to Phase 3 execution)

- The exact list of missing fixtures — must be produced by running the audit script, not predicted.
- Whether `LotCatalogDto` is genuinely unported or lives under a different name in `ab.api.models.lots` — the guide will either port it or declare it out-of-scope after a close read during execution.
- Whether any endpoint body currently bypasses `RequestModel` validation — the audit will flag, and the fix is out-of-scope for this feature unless it blocks a Lotsdb call site.

## Open Questions

None. All Technical Context items are resolved; no `NEEDS CLARIFICATION` remain.
