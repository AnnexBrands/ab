"""Example: Webhook operations (6 endpoints).

Note: These are server-side callback receivers. Stripe/Twilio call these
endpoints on the ACPortal server. This example is for testing only.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Webhooks", env="staging")

runner.add(
    "stripe_handle",
    lambda api: api.webhooks.stripe_handle(),
)

runner.add(
    "stripe_connect_handle",
    lambda api: api.webhooks.stripe_connect_handle(),
)

runner.add(
    "stripe_checkout_completed",
    lambda api: api.webhooks.stripe_checkout_completed(),
)

runner.add(
    "twilio_body_sms_inbound",
    lambda api: api.webhooks.twilio_body_sms_inbound(),
)

runner.add(
    "twilio_form_sms_inbound",
    lambda api: api.webhooks.twilio_form_sms_inbound(),
)

runner.add(
    "twilio_sms_status_callback",
    lambda api: api.webhooks.twilio_sms_status_callback(),
)

if __name__ == "__main__":
    runner.run()
