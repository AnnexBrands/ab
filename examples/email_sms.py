"""Example: Email & SMS communication operations (8 methods).

Covers send_email, send_document_email, create_transactional_email,
send_template_email, list_sms, send_sms, mark_sms_read, get_sms_template.
"""

from examples._runner import ExampleRunner
from tests.constants import TEST_JOB_DISPLAY_ID

runner = ExampleRunner("Email & SMS", env="staging")

# ═══════════════════════════════════════════════════════════════════════
# Email
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "send_email",
    lambda api: api.jobs.send_email(
        TEST_JOB_DISPLAY_ID,
        to=["test@example.com"],
        subject="Test email via SDK",
        body="Hello from ABConnect SDK",
    ),
)

runner.add(
    "send_document_email",
    lambda api, data=None: api.jobs.send_document_email(TEST_JOB_DISPLAY_ID, data=data or {}),
    request_model="SendDocumentEmailModel",
    request_fixture_file="SendDocumentEmailModel.json",
)

runner.add(
    "create_transactional_email",
    lambda api: api.jobs.create_transactional_email(TEST_JOB_DISPLAY_ID),
)

runner.add(
    "send_template_email",
    lambda api: api.jobs.send_template_email(TEST_JOB_DISPLAY_ID, "TEMPLATE_GUID"),
)

# ═══════════════════════════════════════════════════════════════════════
# SMS
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list_sms",
    lambda api: api.jobs.list_sms(TEST_JOB_DISPLAY_ID),
)

runner.add(
    "send_sms",
    lambda api, data=None: api.jobs.send_sms(TEST_JOB_DISPLAY_ID, data=data or {}),
    request_model="SendSMSModel",
    request_fixture_file="SendSMSModel.json",
)

runner.add(
    "mark_sms_read",
    lambda api, data=None: api.jobs.mark_sms_read(TEST_JOB_DISPLAY_ID, data=data or {}),
    request_model="MarkSmsAsReadModel",
    request_fixture_file="MarkSmsAsReadModel.json",
)

runner.add(
    "get_sms_template",
    lambda api: api.jobs.get_sms_template(TEST_JOB_DISPLAY_ID, "TEMPLATE_ID"),
)

if __name__ == "__main__":
    runner.run()
