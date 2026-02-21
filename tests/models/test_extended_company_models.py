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
from tests.conftest import require_fixture


class TestExtendedCompanyModels:
    def test_company_brand(self):
        data = require_fixture("CompanyBrand", "GET", "/companies/brands")
        CompanyBrand.model_validate(data)

    def test_brand_tree(self):
        data = require_fixture("BrandTree", "GET", "/companies/brandstree")
        BrandTree.model_validate(data)

    def test_geo_settings(self):
        data = require_fixture("GeoSettings", "GET", "/companies/{id}/geosettings")
        GeoSettings.model_validate(data)

    def test_carrier_account(self):
        data = require_fixture("CarrierAccount", "GET", "/companies/{id}/carrierAcounts")
        CarrierAccount.model_validate(data)

    def test_packaging_settings(self):
        data = require_fixture("PackagingSettings", "GET", "/companies/{id}/packagingsettings")
        PackagingSettings.model_validate(data)

    def test_packaging_labor(self):
        data = require_fixture("PackagingLabor", "GET", "/companies/{id}/packaginglabor")
        PackagingLabor.model_validate(data)

    def test_packaging_tariff(self):
        data = require_fixture("PackagingTariff", "GET", "/companies/{id}/inheritedPackagingTariffs")
        PackagingTariff.model_validate(data)
