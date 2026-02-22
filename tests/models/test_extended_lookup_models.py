"""Fixture validation tests for extended Lookup models."""

from ab.api.models.lookup import AccessKey, DensityClassEntry, LookupValue, ParcelPackageType
from tests.conftest import assert_no_extra_fields, require_fixture


class TestExtendedLookupModels:
    def test_lookup_value(self):
        data = require_fixture("LookupValue", "GET", "/lookup/{masterConstantKey}")
        model = LookupValue.model_validate(data)
        assert isinstance(model, LookupValue)
        assert_no_extra_fields(model)

    def test_access_key(self):
        data = require_fixture("AccessKey", "GET", "/lookup/accessKeys")
        model = AccessKey.model_validate(data)
        assert isinstance(model, AccessKey)
        assert_no_extra_fields(model)

    def test_parcel_package_type(self):
        data = require_fixture("ParcelPackageType", "GET", "/lookup/parcelPackageTypes")
        model = ParcelPackageType.model_validate(data)
        assert isinstance(model, ParcelPackageType)
        assert_no_extra_fields(model)

    def test_density_class_entry(self):
        data = require_fixture("DensityClassEntry", "GET", "/lookup/densityClassMap")
        model = DensityClassEntry.model_validate(data)
        assert isinstance(model, DensityClassEntry)
        assert_no_extra_fields(model)
