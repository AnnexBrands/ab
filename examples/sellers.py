"""Example: Seller operations (5 methods)."""

from examples._runner import ExampleRunner
from tests.constants import TEST_SELLER_ID

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
    lambda api: api.sellers.get(TEST_SELLER_ID),
    response_model="SellerExpandedDto",
    fixture_file="SellerExpandedDto_detail.json",
)

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "create",
    lambda api, data=None: api.sellers.create(data=data or {}),
    request_model="AddSellerRequest",
    request_fixture_file="AddSellerRequest.json",
    response_model="SellerDto",
    fixture_file="SellerDto.json",
)

runner.add(
    "update",
    lambda api, data=None: api.sellers.update(TEST_SELLER_ID, data=data or {}),
    request_model="UpdateSellerRequest",
    request_fixture_file="UpdateSellerRequest.json",
    response_model="SellerDto",
    fixture_file="SellerDto.json",
)

runner.add(
    "delete",
    lambda api: api.sellers.delete(TEST_SELLER_ID),
)

if __name__ == "__main__":
    runner.run()
