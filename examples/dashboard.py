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

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_COMPANY_ID, TEST_VIEW_ID


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
    save("GridViewInfo.json", views)

    # --- Step 2: dashboard summary, all paths --------------------------
    print(f"\n# api.dashboard.get(view_id={TEST_VIEW_ID}, company_id={TEST_COMPANY_ID!r})")
    summary = api.dashboard.get(view_id=TEST_VIEW_ID, company_id=TEST_COMPANY_ID)
    print(format_result(summary))
    save("DashboardSummary.json", summary)

    # --- Step 3: documented "no params" call ---------------------------
    # Swagger marks both viewId and companyId optional. The API defaults
    # companyId to the active user's primary company; this call must NOT
    # raise.
    print("\n# api.dashboard.get()  (no params -- defaults to active user's primary company)")
    default_summary = api.dashboard.get()
    print(format_result(default_summary))

    # --- Step 4: saved grid-view state (column / filter / sort) ---------
    # The GET endpoints take a *str* view_id (path param {id}); TEST_VIEW_ID
    # is the int row id discovered above, so pass str(...).
    print(f"\n# api.dashboard.get_grid_view_state(view_id={str(TEST_VIEW_ID)!r})")
    state = api.dashboard.get_grid_view_state(str(TEST_VIEW_ID))
    print(format_result(state))
    save("GridViewState.json", state)

    # save_grid_view_state is state-changing -- guarded. resp="-" (no model), no save.
    if mutations_enabled():
        print(f"\n# api.dashboard.save_grid_view_state(view_id={str(TEST_VIEW_ID)!r}, data=...)")
        save_res = api.dashboard.save_grid_view_state(
            str(TEST_VIEW_ID), data=load_request("GridViewState.json")
        )
        print(format_result(save_res))
    else:
        print(
            "# api.dashboard.save_grid_view_state skipped -- set AB_RUN_MUTATIONS=1 "
            "to run (mutates staging)"
        )

    # --- Step 5: dashboard grid feeds -----------------------------------
    # POST endpoints that take a DashboardCompanyRequest filter body and return
    # raw grid rows (no typed response model -- print only, no save). Read-only
    # feeds, so called unguarded with the captured request fixture.
    feed_body = load_request("DashboardCompanyRequest.json")

    print("\n# api.dashboard.inbound(data=...)")
    print(format_result(api.dashboard.inbound(data=feed_body)))

    print("\n# api.dashboard.outbound(data=...)")
    print(format_result(api.dashboard.outbound(data=feed_body)))

    print("\n# api.dashboard.in_house(data=...)")
    print(format_result(api.dashboard.in_house(data=feed_body)))

    print("\n# api.dashboard.local_deliveries(data=...)")
    print(format_result(api.dashboard.local_deliveries(data=feed_body)))

    print("\n# api.dashboard.recent_estimates(data=...)")
    print(format_result(api.dashboard.recent_estimates(data=feed_body)))


if __name__ == "__main__":
    main()
