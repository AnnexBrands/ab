"""Example: Seller operations (5 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Sellers", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "list",
    lambda api: api.sellers.list(page=1, page_size=25),
    response_model="PaginatedList[SellerExpandedDto]",
    fixture_file="SellerExpandedDto.json",
)

runner.add(
    "get",
    lambda api: api.sellers.get(1),
    response_model="SellerExpandedDto",
    fixture_file="SellerExpandedDto_detail.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "create",
    lambda api: api.sellers.create(
        # TODO: capture fixture — needs valid AddSellerRequest body
        {},
    ),
    request_model="AddSellerRequest",
    response_model="SellerDto",
)

runner.add(
    "update",
    lambda api: api.sellers.update(
        1,
        # TODO: capture fixture — needs valid UpdateSellerRequest body
        {},
    ),
    request_model="UpdateSellerRequest",
    response_model="SellerDto",
)

runner.add(
    "delete",
    lambda api: api.sellers.delete(
        # TODO: destructive — no fixture needed
        1,
    ),
)

if __name__ == "__main__":
    runner.run()
