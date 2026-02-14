"""Live integration tests for Contacts API (T071)."""

import pytest

from tests.constants import LIVE_CONTACT_ID

pytestmark = pytest.mark.live


class TestContactsIntegration:
    def test_get_contact(self, api):
        result = api.contacts.get(str(LIVE_CONTACT_ID))
        assert result is not None

    def test_get_details(self, api):
        result = api.contacts.get_details(str(LIVE_CONTACT_ID))
        assert result is not None

    def test_get_primary_details(self, api):
        result = api.contacts.get_primary_details(str(LIVE_CONTACT_ID))
        assert result is not None

    def test_get_current_user(self, api):
        result = api.contacts.get_current_user()
        assert result is not None
