"""Example: Catalog operations (6 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Catalog", env="staging")

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "list",
    lambda api: api.catalog.list(page=1, page_size=25),
    response_model="PaginatedList[CatalogExpandedDto]",
    fixture_file="CatalogExpandedDto.json",
)

runner.add(
    "get",
    lambda api: api.catalog.get(1),
    response_model="CatalogExpandedDto",
    fixture_file="CatalogExpandedDto.json",
)

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "create",
    lambda api, data=None: api.catalog.create(data or {}),
    request_model="AddCatalogRequest",
    request_fixture_file="AddCatalogRequest.json",
    response_model="CatalogWithSellersDto",
    fixture_file="CatalogWithSellersDto.json",
)

runner.add(
    "update",
    lambda api, data=None: api.catalog.update(1, data or {}),
    request_model="UpdateCatalogRequest",
    request_fixture_file="UpdateCatalogRequest.json",
    response_model="CatalogWithSellersDto",
    fixture_file="CatalogWithSellersDto.json",
)

runner.add(
    "delete",
    lambda api: api.catalog.delete(1),
)

runner.add(
    "bulk_insert",
    lambda api, data=None: api.catalog.bulk_insert(data or {}),
    request_model="BulkInsertRequest",
    request_fixture_file="BulkInsertRequest.json",
)

if __name__ == "__main__":
    runner.run()
