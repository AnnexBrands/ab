"""Fixture validation tests for Contact models (T060)."""

import pytest

from tests.conftest import require_fixture

from ab.api.models.contacts import (
    ContactDetailedInfo,
    ContactPrimaryDetails,
    ContactSimple,
    SearchContactEntityResult,
)


class TestContactModels:
    @pytest.mark.live
    def test_contact_simple(self):
        data = require_fixture("ContactSimple", "GET", "/contacts/user", required=True)
        model = ContactSimple.model_validate(data)
        # /contacts/user may not return id — assert at least one name field
        assert model.id is not None or model.full_name is not None

    @pytest.mark.live
    def test_contact_detailed_info(self):
        data = require_fixture("ContactDetailedInfo", "GET", "/contacts/{id}/editdetails", required=True)
        model = ContactDetailedInfo.model_validate(data)
        assert model.id is not None

    @pytest.mark.live
    def test_contact_primary_details(self):
        data = require_fixture("ContactPrimaryDetails", "GET", "/contacts/{id}/primarydetails", required=True)
        model = ContactPrimaryDetails.model_validate(data)
        assert model.full_name is not None

    @pytest.mark.live
    def test_search_contact_entity_result(self):
        data = require_fixture("SearchContactEntityResult", "POST", "/contacts/v2/search", required=True)
        model = SearchContactEntityResult.model_validate(data)
        assert model.id is not None or model.full_name is not None
