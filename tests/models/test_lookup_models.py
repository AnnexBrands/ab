"""Fixture validation tests for Lookup models (T063)."""

import pytest

from ab.api.models.address import AddressIsValidResult, PropertyType
from ab.api.models.lookup import ContactTypeEntity, CountryCodeDto, JobStatus, LookupItem
from tests.conftest import require_fixture


class TestLookupModels:
    @pytest.mark.live
    def test_contact_type_entity(self):
        data = require_fixture("ContactTypeEntity", "GET", "/lookup/contacttypes", required=True)
        model = ContactTypeEntity.model_validate(data)
        assert model.id is not None

    @pytest.mark.live
    def test_country_code_dto(self):
        data = require_fixture("CountryCodeDto", "GET", "/lookup/countries", required=True)
        CountryCodeDto.model_validate(data)

    @pytest.mark.live
    def test_job_status(self):
        data = require_fixture("JobStatus", "GET", "/lookup/jobstatuses", required=True)
        JobStatus.model_validate(data)

    def test_lookup_item(self):
        data = require_fixture("LookupItem", "GET", "/lookup/items")
        LookupItem.model_validate(data)

    def test_address_is_valid_result(self):
        data = require_fixture("AddressIsValidResult", "GET", "/address/isvalid")
        AddressIsValidResult.model_validate(data)

    def test_property_type(self):
        data = require_fixture("PropertyType", "GET", "/address/propertytype")
        PropertyType.model_validate(data)
