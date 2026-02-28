"""Example: Lot operations (6 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Lots", env="staging")

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "list",
    lambda api: api.lots.list(page=1, page_size=25),
    response_model="PaginatedList[LotDto]",
    fixture_file="LotDto.json",
)

runner.add(
    "get",
    lambda api: api.lots.get(1),
    response_model="LotDto",
    fixture_file="LotDto.json",
)

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "create",
    lambda api, data=None: api.lots.create(data=data or {}),
    request_model="AddLotRequest",
    request_fixture_file="AddLotRequest.json",
    response_model="LotDto",
    fixture_file="LotDto.json",
)

runner.add(
    "update",
    lambda api, data=None: api.lots.update(1, data=data or {}),
    request_model="UpdateLotRequest",
    request_fixture_file="UpdateLotRequest.json",
    response_model="LotDto",
    fixture_file="LotDto.json",
)

runner.add(
    "delete",
    lambda api: api.lots.delete(1),
)

runner.add(
    "get_overrides",
    lambda api: api.lots.get_overrides([]),
    response_model="List[LotOverrideDto]",
    fixture_file="LotOverrideDto.json",
)

if __name__ == "__main__":
    runner.run()
