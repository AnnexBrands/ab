"""Example: AutoPrice operations (requires ABC API access_key)."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# Quick quote
quote = api.autoprice.quick_quote({
    "originZip": "43213",
    "destinationZip": "90210",
    "weight": 150,
})
print(f"Quick quote: {quote}")

# Full quote request
result = api.autoprice.quote_request({
    "originZip": "43213",
    "destinationZip": "90210",
    "items": [{"weight": 150, "class": "70"}],
})
print(f"Quote request: {result}")
