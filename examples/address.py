"""Example: Address operations (2 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Address", env="staging")

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "validate",
    lambda api: api.address.validate(
        # TODO: capture fixture — needs valid street, city, state, zipCode
        Line1="12742 E Caley Av",
        City="Centennial",
        State="CO",
        ZipCode="80111",
        Country="US",
    ),
    response_model="AddressIsValidResult",
    fixture_file="AddressIsValidResult.json",
)

runner.add(
    "get_property_type",
    lambda api: api.address.get_property_type(
        # TODO: capture fixture — needs valid street + zipCode for real address
        street="123 Main St",
        zip_code="43213",
    ),
    response_model="PropertyType",
    fixture_file="PropertyType.json",
)

if __name__ == "__main__":
    runner.run()
