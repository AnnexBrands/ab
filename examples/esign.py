"""Example: E-Sign operations (2 endpoints)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("E-Sign", env="staging")

runner.add(
    "get_result",
    lambda api: api.esign.get_result(envelope="test-envelope", event="signing_complete"),
    response_model="ESignResult",
    fixture_file="ESignResult.json",
)

runner.add(
    "get_esign",
    lambda api: api.esign.get_esign(100001, "booking-key-123"),
    response_model="ESignData",
    fixture_file="ESignData.json",
)

if __name__ == "__main__":
    runner.run()
