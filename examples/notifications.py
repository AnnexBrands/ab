"""Example: Notifications operations (1 endpoint)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Notifications", env="staging")

runner.add(
    "get_all",
    lambda api: api.notifications.get_all(),
    response_model="List[Notification]",
    fixture_file="Notification.json",
)

if __name__ == "__main__":
    runner.run()
