"""Fixture validation tests for extended Company models."""

from ab.api.models.companies import (
    BrandTree,
    CarrierAccount,
    CompanyBrand,
    GeoSettings,
    PackagingLabor,
    PackagingSettings,
    PackagingTariff,
)
from tests.conftest import assert_no_extra_fields, require_fixture


class TestExtendedCompanyModels:
    def test_company_brand(self):
        data = require_fixture("CompanyBrand", "GET", "/companies/brands")
        model = CompanyBrand.model_validate(data)
        assert isinstance(model, CompanyBrand)
        assert_no_extra_fields(model)

    def test_brand_tree(self):
        data = require_fixture("BrandTree", "GET", "/companies/brandstree")
        model = BrandTree.model_validate(data)
        assert isinstance(model, BrandTree)
        assert_no_extra_fields(model)

    def test_geo_settings(self):
        data = require_fixture("GeoSettings", "GET", "/companies/{id}/geosettings")
        model = GeoSettings.model_validate(data)
        assert isinstance(model, GeoSettings)
        assert_no_extra_fields(model)

    def test_carrier_account(self):
        data = require_fixture("CarrierAccount", "GET", "/companies/{id}/carrierAcounts")
        model = CarrierAccount.model_validate(data)
        assert isinstance(model, CarrierAccount)
        assert_no_extra_fields(model)

    def test_packaging_settings(self):
        data = require_fixture("PackagingSettings", "GET", "/companies/{id}/packagingsettings")
        model = PackagingSettings.model_validate(data)
        assert isinstance(model, PackagingSettings)
        assert_no_extra_fields(model)

    def test_packaging_labor(self):
        data = require_fixture("PackagingLabor", "GET", "/companies/{id}/packaginglabor")
        model = PackagingLabor.model_validate(data)
        assert isinstance(model, PackagingLabor)
        assert_no_extra_fields(model)

    def test_packaging_tariff(self):
        data = require_fixture("PackagingTariff", "GET", "/companies/{id}/inheritedPackagingTariffs")
        model = PackagingTariff.model_validate(data)
        assert isinstance(model, PackagingTariff)
        assert_no_extra_fields(model)
