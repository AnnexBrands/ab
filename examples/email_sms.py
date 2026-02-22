"""Example: Email & SMS communication operations (8 methods).

Covers send_email, send_document_email, create_transactional_email,
send_template_email, list_sms, send_sms, mark_sms_read, get_sms_template.
"""

from examples._runner import ExampleRunner
from tests.constants import LIVE_JOB_DISPLAY_ID

runner = ExampleRunner("Email & SMS", env="staging")

# ═══════════════════════════════════════════════════════════════════════
# Email
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "send_email",
    lambda api: api.jobs.send_email(
        LIVE_JOB_DISPLAY_ID,
        to=["test@example.com"],
        subject="Test email via SDK",
        body="Hello from ABConnect SDK",
    ),
)

runner.add(
    "send_document_email",
    lambda api: api.jobs.send_document_email(
        LIVE_JOB_DISPLAY_ID,
        to=["test@example.com"],
        subject="Document email",
        documentType="BOL",
    ),
    request_model="SendDocumentEmailModel",
)

runner.add(
    "create_transactional_email",
    lambda api: api.jobs.create_transactional_email(LIVE_JOB_DISPLAY_ID),
)

runner.add(
    "send_template_email",
    lambda api: api.jobs.send_template_email(LIVE_JOB_DISPLAY_ID, "TEMPLATE_GUID"),
)

# ═══════════════════════════════════════════════════════════════════════
# SMS
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list_sms",
    lambda api: api.jobs.list_sms(LIVE_JOB_DISPLAY_ID),
)

runner.add(
    "send_sms",
    lambda api: api.jobs.send_sms(
        LIVE_JOB_DISPLAY_ID,
        phoneNumber="5551234567",
        message="Test SMS via SDK",
    ),
    request_model="SendSMSModel",
)

runner.add(
    "mark_sms_read",
    lambda api: api.jobs.mark_sms_read(
        LIVE_JOB_DISPLAY_ID,
        smsIds=["SMS_ID"],
    ),
    request_model="MarkSmsAsReadModel",
)

runner.add(
    "get_sms_template",
    lambda api: api.jobs.get_sms_template(LIVE_JOB_DISPLAY_ID, "TEMPLATE_ID"),
)

if __name__ == "__main__":
    runner.run()
