"""Example: Views/grids management operations (8 methods).

Covers list, get, create, delete, access info, update access,
dataset SPs listing and detail.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Views", env="staging")

TEST_VIEW_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# Views CRUD
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list",
    lambda api: api.views.list(),
    response_model="List[GridViewDetails]",
    fixture_file="GridViewDetails.json",
)

runner.add(
    "get",
    lambda api: api.views.get(TEST_VIEW_ID),
    response_model="GridViewDetails",
)

runner.add(
    "create",
    lambda api, data=None: api.views.create(**(data or {})),
    request_model="GridViewCreateRequest",
    request_fixture_file="GridViewCreateRequest.json",
    response_model="GridViewDetails",
)

runner.add(
    "delete",
    lambda api: api.views.delete(TEST_VIEW_ID),
    response_model="ServiceBaseResponse",
)

# ═══════════════════════════════════════════════════════════════════════
# Access Control
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get_access_info",
    lambda api: api.views.get_access_info(TEST_VIEW_ID),
    response_model="GridViewAccess",
    fixture_file="GridViewAccess.json",
)

runner.add(
    "update_access",
    lambda api: api.views.update_access(TEST_VIEW_ID, users=[], roles=[]),
)

# ═══════════════════════════════════════════════════════════════════════
# Dataset Stored Procedures
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get_dataset_sps",
    lambda api: api.views.get_dataset_sps(),
    response_model="List[StoredProcedureColumn]",
    fixture_file="StoredProcedureColumn.json",
)

runner.add(
    "get_dataset_sp",
    lambda api: api.views.get_dataset_sp("spName"),
    response_model="List[StoredProcedureColumn]",
)

if __name__ == "__main__":
    runner.run()
