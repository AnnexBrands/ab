"""Fixture validation tests for Contact models."""

import pytest

from ab.api.models.contacts import (
    ContactDetailedInfo,
    ContactPrimaryDetails,
    ContactSimple,
    SearchContactEntityResult,
)
from tests.conftest import assert_no_extra_fields, require_fixture


class TestContactModels:
    @pytest.mark.live
    def test_contact_simple(self):
        data = require_fixture("ContactSimple", "GET", "/contacts/user", required=True)
        model = ContactSimple.model_validate(data)
        assert isinstance(model, ContactSimple)
        assert_no_extra_fields(model)

    @pytest.mark.live
    def test_contact_detailed_info(self):
        data = require_fixture("ContactDetailedInfo", "GET", "/contacts/{id}/editdetails", required=True)
        model = ContactDetailedInfo.model_validate(data)
        assert isinstance(model, ContactDetailedInfo)
        assert_no_extra_fields(model)

    @pytest.mark.live
    def test_contact_primary_details(self):
        data = require_fixture("ContactPrimaryDetails", "GET", "/contacts/{id}/primarydetails", required=True)
        model = ContactPrimaryDetails.model_validate(data)
        assert isinstance(model, ContactPrimaryDetails)
        assert_no_extra_fields(model)
        assert model.full_name is not None

    def test_search_contact_entity_result(self):
        data = require_fixture("SearchContactEntityResult", "POST", "/contacts/v2/search", required=True)
        if isinstance(data, list):
            data = data[0]
        model = SearchContactEntityResult.model_validate(data)
        assert isinstance(model, SearchContactEntityResult)
        assert_no_extra_fields(model)
