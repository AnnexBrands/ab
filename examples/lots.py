"""Example: Lot operations (6 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Lots", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

# (none — all lot methods need request data or valid IDs)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "list",
    lambda api: api.lots.list(page=1, page_size=25),
    # TODO: capture fixture — needs valid catalog ID param to return results
    response_model="PaginatedList[LotDto]",
)

runner.add(
    "get",
    lambda api: api.lots.get(
        # TODO: capture fixture — needs valid lot ID
        1,
    ),
    response_model="LotDto",
)

runner.add(
    "create",
    lambda api: api.lots.create(
        # TODO: capture fixture — needs valid AddLotRequest body
        {},
    ),
    request_model="AddLotRequest",
    response_model="LotDto",
)

runner.add(
    "update",
    lambda api: api.lots.update(
        1,
        # TODO: capture fixture — needs valid UpdateLotRequest body
        {},
    ),
    request_model="UpdateLotRequest",
    response_model="LotDto",
)

runner.add(
    "delete",
    lambda api: api.lots.delete(
        # TODO: destructive — no fixture needed
        1,
    ),
)

runner.add(
    "get_overrides",
    lambda api: api.lots.get_overrides(
        # TODO: capture fixture — needs valid customer item IDs
        [],
    ),
    response_model="List[LotOverrideDto]",
)

if __name__ == "__main__":
    runner.run()
