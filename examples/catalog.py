"""Example: Catalog operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# List all catalogs
catalogs = api.catalog.list()
print(f"Catalogs: {catalogs}")

# Get a specific catalog
catalog = api.catalog.get(1)
print(f"Catalog: {catalog}")
