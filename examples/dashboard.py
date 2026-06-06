"""Example: Dashboard operations.

Live SDK example -- no runner indirection. Run with valid staging
credentials in ``.env.staging`` to hit the real API and (optionally) save
captured responses as fixtures under ``tests/fixtures/``.

Operator-in-the-loop sequence
-----------------------------

If you do not yet have a ``TEST_VIEW_ID``, follow this discovery chain:

1. Call ``api.dashboard.get_grid_views()`` first. It returns
   ``List[GridViewInfo]`` (swagger ``GridViewDetails``: ``id``, ``name``,
   ``dataKey``, ``isActive``).
2. Pick the ``id`` of a view that is ``isActive`` and matches the dataset
   you want -- e.g. "Inbound" -> dataKey ``inbound``.
3. Set ``TEST_VIEW_ID`` in ``examples/constants.py`` to that ``id``.
4. Re-run this example to capture ``DashboardSummary.json``.

Forward reference: ``GridViewInfo.id`` (output of ``GET /dashboard/gridviews``)
is the value passed as ``DashboardParams.view_id`` to ``GET /dashboard``.

Swagger vs. live behaviour
--------------------------

* Swagger documents ``companyId`` as a query parameter on ``GET /dashboard``.
* The parameter is **not required** in swagger, and the live API does not
  fail when it is omitted -- it defaults to the active user's primary
  company. The unit tests under ``tests/unit/test_dashboard.py`` document
  this with explicit assertions.

See also: https://ab-sdk.readthedocs.io/en/latest/api/dashboard.html
"""

from __future__ import annotations

import json

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import capture_dir
from examples.constants import TEST_COMPANY_ID, TEST_VIEW_ID

# Honors AB_EXAMPLE_CAPTURE_DIR so the verify harness writes to a temp dir, never
# overwriting committed fixtures (feature 037).
FIXTURES_DIR = capture_dir()


def _save(name: str, payload) -> None:
    """Serialise *payload* (Pydantic model or list) to ``tests/fixtures/{name}``."""
    from pydantic import BaseModel

    if isinstance(payload, list):
        data = [
            item.model_dump(by_alias=True, mode="json") if isinstance(item, BaseModel) else item
            for item in payload
        ]
    elif isinstance(payload, BaseModel):
        data = payload.model_dump(by_alias=True, mode="json")
    else:
        data = payload
    out = FIXTURES_DIR / name
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"  saved -> {out}")


def main() -> None:
    api = ABConnectAPI(env="staging")

    # Output formatting goes through ``ab.cli.formatter.format_result`` so the
    # ``abs dashboard …`` CLI and this example produce identical output. The
    # per-row / per-summary layout lives on ``GridViewInfo.cli_format`` and
    # ``DashboardSummary.cli_format``; pass ``as_json=True`` for the legacy
    # JSON dump.

    # --- Step 1: discover available view IDs ---------------------------
    print("\n# api.dashboard.get_grid_views()")
    views = api.dashboard.get_grid_views()
    print(format_result(views))
    _save("GridViewInfo.json", views)

    # --- Step 2: dashboard summary, all paths --------------------------
    print(f"\n# api.dashboard.get(view_id={TEST_VIEW_ID}, company_id={TEST_COMPANY_ID!r})")
    summary = api.dashboard.get(view_id=TEST_VIEW_ID, company_id=TEST_COMPANY_ID)
    print(format_result(summary))
    _save("DashboardSummary.json", summary)

    # --- Step 3: documented "no params" call ---------------------------
    # Swagger marks both viewId and companyId optional. The API defaults
    # companyId to the active user's primary company; this call must NOT
    # raise.
    print("\n# api.dashboard.get()  (no params -- defaults to active user's primary company)")
    default_summary = api.dashboard.get()
    print(format_result(default_summary))


if __name__ == "__main__":
    main()
