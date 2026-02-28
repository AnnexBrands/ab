"""Example: Dashboard operations (9 methods).

Covers dashboard summary, grid views, grid view state, and operational
panels (inbound, in-house, outbound, local deliveries, recent estimates).
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Dashboard", env="staging")

TEST_VIEW_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# Dashboard
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get",
    lambda api: api.dashboard.get(),
    response_model="DashboardSummary",
    fixture_file="DashboardSummary.json",
)

runner.add(
    "get_grid_views",
    lambda api: api.dashboard.get_grid_views(),
    response_model="List[GridViewInfo]",
    fixture_file="GridViewInfo.json",
)

runner.add(
    "get_grid_view_state",
    lambda api: api.dashboard.get_grid_view_state(TEST_VIEW_ID),
    response_model="GridViewState",
    fixture_file="GridViewState.json",
)

runner.add(
    "save_grid_view_state",
    lambda api, data=None: api.dashboard.save_grid_view_state(
        TEST_VIEW_ID, data=data or {"columns": [], "filters": []},
    ),
)

runner.add(
    "inbound",
    lambda api, data=None: api.dashboard.inbound(data=data or {}),
)

runner.add(
    "in_house",
    lambda api, data=None: api.dashboard.in_house(data=data or {}),
)

runner.add(
    "outbound",
    lambda api, data=None: api.dashboard.outbound(data=data or {}),
)

runner.add(
    "local_deliveries",
    lambda api, data=None: api.dashboard.local_deliveries(data=data or {}),
)

runner.add(
    "recent_estimates",
    lambda api, data=None: api.dashboard.recent_estimates(data=data or {}),
)

if __name__ == "__main__":
    runner.run()
