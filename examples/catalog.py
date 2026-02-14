"""Example: Catalog operations (6 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Catalog", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

# (none — all catalog methods need request data or return empty results)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "list",
    lambda api: api.catalog.list(page=1, page_size=25),
    # TODO: capture fixture — returns empty on staging
    response_model="PaginatedList[CatalogExpandedDto]",
)

runner.add(
    "get",
    lambda api: api.catalog.get(
        # TODO: capture fixture — needs valid catalog ID
        1,
    ),
    response_model="CatalogExpandedDto",
)

runner.add(
    "create",
    lambda api: api.catalog.create(
        # TODO: capture fixture — needs valid AddCatalogRequest body
        {},
    ),
    request_model="AddCatalogRequest",
    response_model="CatalogWithSellersDto",
)

runner.add(
    "update",
    lambda api: api.catalog.update(
        1,
        # TODO: capture fixture — needs valid UpdateCatalogRequest body
        {},
    ),
    request_model="UpdateCatalogRequest",
    response_model="CatalogWithSellersDto",
)

runner.add(
    "delete",
    lambda api: api.catalog.delete(
        # TODO: destructive — no fixture needed
        1,
    ),
)

runner.add(
    "bulk_insert",
    lambda api: api.catalog.bulk_insert(
        # TODO: capture fixture — needs valid BulkInsertRequest body
        {},
    ),
    request_model="BulkInsertRequest",
)

if __name__ == "__main__":
    runner.run()
