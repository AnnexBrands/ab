"""Example: Seller operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# List sellers
sellers = api.sellers.list()
print(f"Sellers: {sellers}")

# Get a specific seller
seller = api.sellers.get(1)
print(f"Seller: {seller.name}")
