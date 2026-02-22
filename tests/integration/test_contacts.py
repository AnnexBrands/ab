"""Live integration tests for Contacts API."""

import pytest

from ab.api.models.contacts import ContactDetailedInfo, ContactPrimaryDetails, ContactSimple
from tests.conftest import assert_no_extra_fields
from tests.constants import TEST_CONTACT_ID

pytestmark = pytest.mark.live


class TestContactsIntegration:
    def test_get_contact(self, api):
        result = api.contacts.get(str(TEST_CONTACT_ID))
        assert isinstance(result, ContactSimple)
        assert_no_extra_fields(result)

    def test_get_details(self, api):
        result = api.contacts.get_details(str(TEST_CONTACT_ID))
        assert isinstance(result, ContactDetailedInfo)
        # ContactDetailedInfo not yet fully typed — skip extra_fields check

    def test_get_primary_details(self, api):
        result = api.contacts.get_primary_details(str(TEST_CONTACT_ID))
        assert isinstance(result, ContactPrimaryDetails)
        assert_no_extra_fields(result)
        assert result.full_name is not None

    def test_get_current_user(self, api):
        result = api.contacts.get_current_user()
        assert isinstance(result, ContactSimple)
        assert_no_extra_fields(result)
