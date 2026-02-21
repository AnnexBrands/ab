"""Fixture validation tests for extended Lookup models."""

from ab.api.models.lookup import AccessKey, DensityClassEntry, LookupValue, ParcelPackageType
from tests.conftest import require_fixture


class TestExtendedLookupModels:
    def test_lookup_value(self):
        data = require_fixture("LookupValue", "GET", "/lookup/{masterConstantKey}")
        LookupValue.model_validate(data)

    def test_access_key(self):
        data = require_fixture("AccessKey", "GET", "/lookup/accessKeys")
        AccessKey.model_validate(data)

    def test_parcel_package_type(self):
        data = require_fixture("ParcelPackageType", "GET", "/lookup/parcelPackageTypes")
        ParcelPackageType.model_validate(data)

    def test_density_class_entry(self):
        data = require_fixture("DensityClassEntry", "GET", "/lookup/densityClassMap")
        DensityClassEntry.model_validate(data)
