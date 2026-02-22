"""Example: Address operations (2 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Address", env="staging")

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "validate",
    lambda api, data=None: api.address.validate(**(data or {})),
    request_model="AddressValidateParams",
    request_fixture_file="AddressValidateParams.json",
    response_model="AddressIsValidResult",
    fixture_file="AddressIsValidResult.json",
)

runner.add(
    "get_property_type",
    lambda api, data=None: api.address.get_property_type(**(data or {})),
    request_model="AddressPropertyTypeParams",
    request_fixture_file="AddressPropertyTypeParams.json",
    response_model="int",
    fixture_file="PropertyType.json",
)

if __name__ == "__main__":
    runner.run()
