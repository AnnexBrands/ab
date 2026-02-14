"""Fixture validation tests for Contact models (T060)."""

import pytest

from tests.conftest import load_fixture

from ab.api.models.contacts import (
    ContactDetailedInfo,
    ContactPrimaryDetails,
    ContactSimple,
    SearchContactEntityResult,
)


class TestContactModels:
    @pytest.mark.live
    def test_contact_simple(self):
        data = load_fixture("ContactSimple")
        model = ContactSimple.model_validate(data)
        # /contacts/user may not return id — assert at least one name field
        assert model.id is not None or model.full_name is not None

    @pytest.mark.live
    def test_contact_detailed_info(self):
        data = load_fixture("ContactDetailedInfo")
        model = ContactDetailedInfo.model_validate(data)
        assert model.id is not None

    @pytest.mark.live
    def test_contact_primary_details(self):
        data = load_fixture("ContactPrimaryDetails")
        model = ContactPrimaryDetails.model_validate(data)
        assert model.full_name is not None

    @pytest.mark.live
    def test_search_contact_entity_result(self):
        data = load_fixture("SearchContactEntityResult")
        model = SearchContactEntityResult.model_validate(data)
        assert model.id is not None or model.full_name is not None
