"""Fixture validation tests for Lookup models (T063)."""

import pytest

from tests.conftest import load_fixture

from ab.api.models.address import AddressIsValidResult, PropertyType
from ab.api.models.lookup import ContactTypeEntity, CountryCodeDto, JobStatus, LookupItem


class TestLookupModels:
    @pytest.mark.live
    def test_contact_type_entity(self):
        data = load_fixture("ContactTypeEntity")
        model = ContactTypeEntity.model_validate(data)
        assert model.id is not None

    @pytest.mark.live
    def test_country_code_dto(self):
        data = load_fixture("CountryCodeDto")
        model = CountryCodeDto.model_validate(data)

    @pytest.mark.live
    def test_job_status(self):
        data = load_fixture("JobStatus")
        model = JobStatus.model_validate(data)

    @pytest.mark.mock
    def test_lookup_item(self):
        data = load_fixture("LookupItem")
        model = LookupItem.model_validate(data)

    @pytest.mark.mock
    def test_address_is_valid_result(self):
        data = load_fixture("AddressIsValidResult")
        model = AddressIsValidResult.model_validate(data)

    @pytest.mark.mock
    def test_property_type(self):
        data = load_fixture("PropertyType")
        model = PropertyType.model_validate(data)
