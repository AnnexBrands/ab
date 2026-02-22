"""Example: Address operations (2 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Address", env="staging")

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "validate",
    lambda api: api.address.validate(
        line1="12742 E Caley Av",
        city="Centennial",
        state="CO",
        zip="80111",
    ),
    response_model="AddressIsValidResult",
    fixture_file="AddressIsValidResult.json",
)

runner.add(
    "get_property_type",
    lambda api: api.address.get_property_type(
        address1="12742 E Caley Av",
        city="Centennial",
        state="CO",
        zip_code="80111",
    ),
    response_model="int",
    fixture_file="PropertyType.json",
)

if __name__ == "__main__":
    runner.run()
