"""Example: ABC Test diagnostic operations (3 endpoints)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("ABC Test", env="staging")

runner.add(
    "get_contact",
    lambda api: api.abc_test.get_contact(),
)

runner.add(
    "get_recent_estimates",
    lambda api: api.abc_test.get_recent_estimates(),
)

runner.add(
    "get_rendered_template",
    lambda api: api.abc_test.get_rendered_template(),
)

if __name__ == "__main__":
    runner.run()
