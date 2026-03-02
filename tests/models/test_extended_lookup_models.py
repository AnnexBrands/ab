"""Fixture validation tests for extended Lookup models."""

import pytest

from ab.api.models.lookup import (
    AccessKey,
    AccessKeySetup,
    CommonInsuranceSlab,
    DensityClassEntry,
    DocumentTypeBySource,
    LookupValue,
    PPCCampaign,
    ParcelPackageType,
)
from tests.conftest import assert_no_extra_fields, require_fixture


def _first_or_skip(data):
    """Return first element of a list fixture, or skip if empty."""
    if isinstance(data, list):
        if not data:
            pytest.skip("Fixture is an empty list — nothing to validate")
        return data[0]
    return data


class TestExtendedLookupModels:
    def test_lookup_value(self):
        data = require_fixture("LookupValue", "GET", "/lookup/{masterConstantKey}")
        item = _first_or_skip(data)
        model = LookupValue.model_validate(item)
        assert isinstance(model, LookupValue)
        assert_no_extra_fields(model)

    def test_access_key(self):
        data = require_fixture("AccessKey", "GET", "/lookup/accessKeys")
        item = _first_or_skip(data)
        model = AccessKey.model_validate(item)
        assert isinstance(model, AccessKey)
        assert_no_extra_fields(model)

    def test_access_key_setup(self):
        data = require_fixture("AccessKeySetup", "GET", "/lookup/accessKey/{accessKey}")
        item = _first_or_skip(data)
        model = AccessKeySetup.model_validate(item)
        assert isinstance(model, AccessKeySetup)
        assert_no_extra_fields(model)

    def test_document_type_by_source(self):
        data = require_fixture("DocumentTypeBySource", "GET", "/lookup/documentTypes")
        item = _first_or_skip(data)
        model = DocumentTypeBySource.model_validate(item)
        assert isinstance(model, DocumentTypeBySource)
        assert_no_extra_fields(model)

    def test_ppc_campaign(self):
        data = require_fixture("PPCCampaign", "GET", "/lookup/PPCCampaigns")
        item = _first_or_skip(data)
        model = PPCCampaign.model_validate(item)
        assert isinstance(model, PPCCampaign)
        assert_no_extra_fields(model)

    def test_common_insurance_slab(self):
        data = require_fixture("CommonInsuranceSlab", "GET", "/lookup/comonInsurance")
        item = _first_or_skip(data)
        model = CommonInsuranceSlab.model_validate(item)
        assert isinstance(model, CommonInsuranceSlab)
        assert_no_extra_fields(model)

    def test_parcel_package_type(self):
        data = require_fixture("ParcelPackageType", "GET", "/lookup/parcelPackageTypes")
        item = _first_or_skip(data)
        model = ParcelPackageType.model_validate(item)
        assert isinstance(model, ParcelPackageType)
        assert_no_extra_fields(model)

    def test_density_class_entry(self):
        data = require_fixture("DensityClassEntry", "GET", "/lookup/densityClassMap")
        item = _first_or_skip(data)
        model = DensityClassEntry.model_validate(item)
        assert isinstance(model, DensityClassEntry)
        assert_no_extra_fields(model)
