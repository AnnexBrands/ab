# Changelog

All notable changes to `annex-abconnect` are documented here. This project
adheres to [Semantic Versioning](https://semver.org/) (pre-1.0: minor/patch
per 0.x pragmatics). The package is imported as `ab`.

## [0.1.7] - 2026-06-18

A packaging-hygiene release plus a small model completion. The `ab` import
surface is backward-compatible with `0.1.6`.

### Changed

- **The published package now ships only the `ab` library.** Previous releases
  bundled the entire `examples/` tree (demo/dev scripts, including
  internal/Acme-specific and harness tooling) into both the wheel and sdist.
  `[tool.setuptools.packages.find]` now includes `ab*` only, and a new
  `MANIFEST.in` prunes `examples/`, `scripts/`, `tests/`, `docs/`, and other
  dev trees from the sdist. Installed size drops and no internal scripts leak to
  PyPI consumers. (`ab` package-data — `py.typed`, `api/schemas/*.json` — is
  unchanged.)

### Fixed

- **`BookedDocument` now models the full book-response document object.** Added
  `documentPath`, `documentDescription`, `documentTypeName`, and `errorMessage`
  (alongside the existing `documentId` / `docType` / `byteCode`). On a normal
  book the label is a **path reference** — `documentPath` + `documentDescription`,
  keyed off the PRO in `ServiceBaseResponse.shipmentId` — and `byteCode` is only
  populated when the request sets `documentByteCodeRequired=True`. The missing
  fields previously surfaced as `extra="allow"` warnings (accessible but
  untyped). Verified live (UPS book of job 7107421, PRO `1ZK430390306149813`).

## [0.1.6] - 2026-06-18

A correctness release for shipment booking. Backward-compatible with `0.1.5`
for client construction, auth, and config; the single **Fixed** item changes
the *wire payload* of `api.jobs.shipment.book()` (not its signature).

### Fixed

- **`ShipmentBookRequest` now sends `quoteOptionIndex`/`shipOutDate` (was
  `providerOptionIndex`/`shipDate`) so `shipment.book()` succeeds.** The portal's
  `BookShipmentRequest` schema binds `quoteOptionIndex` for the chosen rate
  option and requires `shipOutDate` for non-UPS carriers; the old aliases were
  never read, so `quoteOptionIndex` defaulted to `0`, the selected provider was
  never set, and every Ready-to-Ship book was rejected with "Specified provider
  was not set or it is not active" (callers saw a phantom success with no
  PRO/label). The Python attributes are renamed to `quote_option_index` /
  `ship_out_date` (construction by attribute or alias both still work). The body
  also gains the schema's optional `internationalParams`,
  `carrierSpecificParams`, and `documentByteCodeRequired` fields. Downstream
  apps that posted a raw dict to work around this can drop the workaround and
  call the typed `book()` again.
- **`ServiceBaseResponse.documents` now accepts document objects, not just
  strings.** A *successful* book returns `documents` as a list of objects
  (`{documentId, docType, byteCode}` — the label byte codes), but the field was
  typed `list[str]`, so the typed `book()` raised a `ValidationError` parsing
  its own success envelope (surfaced live booking UPS job 7036373, PRO
  `1ZK430390312572326`). The field is now `list[str | BookedDocument]`
  (new `BookedDocument` model), so `book()` returns the success envelope
  instead of throwing. Backward-compatible with operations that return
  document URL/reference strings.

## [0.1.5] - 2026-06-15

An example-coverage + ergonomics + correctness release. **Every routed endpoint
now has a canonical plain-script example** (`215 / 215`), six new endpoints and
several SDK ergonomics land, and three correctness fixes harden job-item and
timeline handling. The client-construction, auth, and config surface is
backward-compatible with `0.1.4`; the three **Fixed** items below change
*behavior* (not signatures) — see the notes there. Downstream consumers pinning
`0.1.4` are unaffected until they bump.

### Added

- **`api.jobs.items` — lenient parcel/freight item helpers.** Create / replace /
  update / delete for parcel and freight items with loose-keyword input (unknown
  kwargs are dropped, not rejected) and get-merge-write *replace-all* semantics
  for freight, so editing one item never wipes the others.
- **Six new routed endpoints** — an account group, `jobs.book`, per-shipment
  tracking (`jobs.tracking.shipment`), and document thumbnail / hide.
- **`MasterConstantKey` enum** — discoverable master-constant keys for
  `lookup.get_by_key`.
- **SDK ergonomics** — `MemoryTokenStorage`, raw-`bytes` document uploads,
  anonymous `AccessKey` autoprice quotes, and per-request header injection
  (`extra_headers`).
- **Completed freight item models** — `JobFreightItem` (response) and
  `FreightShipment` (request) now mirror the full swagger `FreightShimpment`
  (31 fields), so a populated freight item validates without drift warnings and a
  get-modify-replace round-trip is lossless. Added `ParcelItemSave`,
  `ParcelItemsRequest`, and `ParcelItemsResponse`.
- **Examples for every routed endpoint** — canonical coverage rises to
  **215 / 215**; `uncovered_endpoints()` and `legacy_only_endpoints()` are both
  empty and the `STRICT_COVERAGE` + `STRICT_NO_LEGACY` gates are `True`. Includes
  examples for the previously-uncovered dashboard reads, `jobs.transfer`,
  `jobs.status`, and the job subgroups (`email`, `sms`, `note`, `on_hold`,
  `parcel_items`, `payment`, `shipment`, `rfq`, `tracking`, `timeline`, `form`,
  `freight_providers`).

### Changed

- **All 114 legacy-only endpoints migrated to canonical examples** — the
  deprecated `examples/_X.py` runner files are superseded by plain-`main()`
  scripts (`catalog`, `commodities`, `commodity_maps`, `companies`(+`_extended`),
  `contacts`(+`_extended`), `documents`, `jobs/core`, `lookup`, `lots`, `notes`,
  `reports`, `rfq`, `shipments`, `views`).

### Fixed

- **Pickup-and-pack agents no longer get a spurious 403 on status-with-note.**
  The timeline status helpers (`api.jobs.tasks.*`) no longer issue a redundant
  `POST /note`: the ABConnect job-management endpoint now records the Job History
  note itself when the task is saved. The old second call required top-level
  note-write permission an agent lacks, so it 403'd and masked an otherwise-
  successful pickup status change. *Behavior change:* the helpers no longer make
  that call; `TimelineHelpers._create_job_history_note` is a deprecated no-op.
- **`api.jobs.parcel_items.create` is now non-destructive (ACID).** `POST
  /job/{id}/parcelitems` is a replace-all (`SaveAllParcelItemsRequest`); the SDK
  previously modeled it as a single-item create, so `create` **wiped the entire
  parcel set**. It now reads the current items, appends, and saves the full set,
  returning the newly added item (`api.jobs.items` builds on this).
- **Empty `2xx` responses no longer raise.** A success response with an empty
  body (common for `DELETE` and replace-all saves) returned "Response was not
  valid JSON"; it now resolves to `None`. *Behavior change:* affected calls (e.g.
  `parcel_items.delete`) return `None` instead of raising.

[0.1.5]: https://github.com/AnnexBrands/ab/compare/v0.1.4...v0.1.5

## [0.1.4] - 2026-06-05

A documents + discoverability release. The `help()` → Read the Docs rollout now
covers every route-backed group, and the Documents endpoint gains a
swagger-faithful item-photo upload. The client-construction, auth, config,
exceptions, and model-import surface relied on by downstream consumers is
unchanged from `0.1.3`.

### Added

- **Item-photo upload for the Documents endpoint** — `documents.upload` is now a
  typed, route-backed `POST /documents` multipart primitive
  (`DocumentUploadRequest` / `DocumentUploadResponse`), with
  `documents.upload_item_photo` and `documents.upload_item_photos` (batch;
  always returns a list) convenience wrappers.
- **`help()` → Read the Docs for every group** — the per-endpoint page + `Docs:`
  footer mechanism (jobs-only in `0.1.3`) now covers all 21 route-backed groups,
  each with generated per-endpoint pages and a `:glob:` toctree.

### Changed

- **`DocumentType` enum corrected to swagger-truth** — values now mirror the live
  `GET /lookup/documentTypes` lookup (e.g. `BOL = 4`, `ITEM_PHOTO = 6`,
  `OTHER = 7`); the previous values were incorrect. Code referencing the old
  members (`UNKNOWN`, `INVOICE`, `PHOTO`, `CLAIM`, `POD`) or their old integer
  values must update.

### Fixed

- Generated per-endpoint pages now escape pipes in the parameter *type* column,
  so Union types (`DocumentType | int`, `str | None`) no longer break the
  Markdown tables under MyST.
- `jobs.tracking.v3` documents `historyAmount` as a **path** parameter (not a
  query parameter) in both its page heading and its docstring footer.

### CI

- Hardened the PyPI publish job: a tag↔`pyproject` version guard, token-based
  auth, and `skip-existing: true`.

[0.1.4]: https://github.com/AnnexBrands/ab/compare/v0.1.3...v0.1.4

## [0.1.3] - 2026-06-05

A quality & discoverability release. No breaking changes — the public API
surface (client construction, auth, config, exceptions, and models) is
backward compatible with `0.1.2`.

### Added

- **Statically discoverable endpoint groups** — `ABConnectAPI` now carries
  class-level annotations for every endpoint group, so `api.<TAB>` completion
  works in editors and REPLs. Adds public `ABConnectAPI.groups()` and
  `__repr__()`.
- **`help()` → Read the Docs links** — route-backed jobs-group methods now
  carry a `Docs:` footer linking to a rich per-endpoint documentation page,
  plus generated per-endpoint pages for the jobs group.
- **`contacts.get_did` accepts integer display IDs** — the parameter is
  widened from `str` to `str | int` (backward compatible; existing string
  callers are unaffected).

### Changed

- Internal quality gates are now enforced in CI: zero `ruff` violations, a
  green deterministic test suite (`pytest -m "not live"`), and no-drift gates
  for the progress report and generated endpoint docs.

[0.1.3]: https://github.com/AnnexBrands/ab/compare/v0.1.2...v0.1.3
