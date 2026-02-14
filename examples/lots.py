"""Example: Lot operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# List all lots
lots = api.lots.list()
print(f"Lots: {lots}")
