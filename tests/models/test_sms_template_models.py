"""Fixture validation tests for SMS Template models (009)."""

from tests.conftest import require_fixture

from ab.api.models.sms_templates import NotificationTokens, SmsTemplate


class TestSmsTemplateModels:
    def test_sms_template(self):
        data = require_fixture("SmsTemplate", "GET", "/SmsTemplate/{templateId}")
        SmsTemplate.model_validate(data)

    def test_notification_tokens(self):
        data = require_fixture("NotificationTokens", "GET", "/SmsTemplate/notificationTokens")
        NotificationTokens.model_validate(data)
