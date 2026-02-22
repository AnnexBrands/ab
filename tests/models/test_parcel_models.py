"""Fixture validation tests for Parcel models."""

from ab.api.models.jobs import PackagingContainer, ParcelItem, ParcelItemWithMaterials
from tests.conftest import assert_no_extra_fields, require_fixture


class TestParcelModels:
    def test_parcel_item(self):
        data = require_fixture("ParcelItem", "GET", "/job/{id}/parcelitems")
        model = ParcelItem.model_validate(data)
        assert isinstance(model, ParcelItem)
        assert_no_extra_fields(model)

    def test_parcel_item_with_materials(self):
        data = require_fixture("ParcelItemWithMaterials", "GET", "/job/{id}/parcel-items-with-materials")
        model = ParcelItemWithMaterials.model_validate(data)
        assert isinstance(model, ParcelItemWithMaterials)
        assert_no_extra_fields(model)

    def test_packaging_container(self):
        data = require_fixture("PackagingContainer", "GET", "/job/{id}/packagingcontainers")
        model = PackagingContainer.model_validate(data)
        assert isinstance(model, PackagingContainer)
        assert_no_extra_fields(model)
