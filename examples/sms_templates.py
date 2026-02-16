"""Example: SMS Template operations (5 endpoints)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("SMS Templates", env="staging")

runner.add(
    "list",
    lambda api: api.sms_templates.list(),
    response_model="List[SmsTemplate]",
    fixture_file="SmsTemplate.json",
)

runner.add(
    "get_notification_tokens",
    lambda api: api.sms_templates.get_notification_tokens(),
    response_model="NotificationTokens",
    fixture_file="NotificationTokens.json",
)

if __name__ == "__main__":
    runner.run()
