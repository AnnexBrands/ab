"""Fixture validation tests for Lookup and Address models."""

import pytest

from ab.api.models.address import AddressIsValidResult
from ab.api.models.lookup import ContactTypeEntity, CountryCodeDto, JobStatus, LookupItem
from tests.conftest import assert_no_extra_fields, require_fixture


class TestLookupModels:
    @pytest.mark.live
    def test_contact_type_entity(self):
        data = require_fixture("ContactTypeEntity", "GET", "/lookup/contacttypes", required=True)
        if isinstance(data, list) and data:
            data = data[0]
        model = ContactTypeEntity.model_validate(data)
        assert isinstance(model, ContactTypeEntity)
        assert_no_extra_fields(model)

    @pytest.mark.live
    def test_country_code_dto(self):
        data = require_fixture("CountryCodeDto", "GET", "/lookup/countries", required=True)
        if isinstance(data, list) and data:
            data = data[0]
        model = CountryCodeDto.model_validate(data)
        assert isinstance(model, CountryCodeDto)
        assert_no_extra_fields(model)

    @pytest.mark.live
    def test_job_status(self):
        data = require_fixture("JobStatus", "GET", "/lookup/jobstatuses", required=True)
        if isinstance(data, list) and data:
            data = data[0]
        model = JobStatus.model_validate(data)
        assert isinstance(model, JobStatus)
        assert_no_extra_fields(model)

    def test_lookup_item(self):
        data = require_fixture("LookupItem", "GET", "/lookup/items")
        if isinstance(data, list) and data:
            data = data[0]
        model = LookupItem.model_validate(data)
        assert isinstance(model, LookupItem)
        assert_no_extra_fields(model)

    def test_address_is_valid_result(self):
        data = require_fixture("AddressIsValidResult", "GET", "/address/isvalid")
        model = AddressIsValidResult.model_validate(data)
        assert isinstance(model, AddressIsValidResult)
        assert_no_extra_fields(model)

    def test_property_type(self):
        data = require_fixture("PropertyType", "GET", "/address/propertytype")
        assert isinstance(data, int)
