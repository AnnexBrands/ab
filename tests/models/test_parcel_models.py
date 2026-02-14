"""Fixture validation tests for Parcel models."""

from tests.conftest import require_fixture

from ab.api.models.jobs import PackagingContainer, ParcelItem, ParcelItemWithMaterials


class TestParcelModels:
    def test_parcel_item(self):
        data = require_fixture("ParcelItem", "GET", "/job/{id}/parcelitems")
        model = ParcelItem.model_validate(data)
        assert model.parcel_item_id is not None
        assert model.description is not None

    def test_parcel_item_with_materials(self):
        data = require_fixture("ParcelItemWithMaterials", "GET", "/job/{id}/parcel-items-with-materials")
        model = ParcelItemWithMaterials.model_validate(data)
        assert model.parcel_item_id is not None
        assert model.materials is not None

    def test_packaging_container(self):
        data = require_fixture("PackagingContainer", "GET", "/job/{id}/packagingcontainers")
        model = PackagingContainer.model_validate(data)
        assert model.container_id is not None
        assert model.name is not None
