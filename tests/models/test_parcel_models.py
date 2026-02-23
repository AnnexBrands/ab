"""Fixture validation tests for Parcel models."""

from ab.api.models.jobs import PackagingContainer, ParcelItem, ParcelItemWithMaterials
from tests.conftest import assert_no_extra_fields, require_fixture


def _validate_fixture(model_cls, data):
    """Validate a fixture that may be a single dict or a JSON array."""
    items = data if isinstance(data, list) else [data]
    assert len(items) > 0, f"Empty fixture for {model_cls.__name__}"
    for item in items:
        model = model_cls.model_validate(item)
        assert isinstance(model, model_cls)
        assert_no_extra_fields(model)


class TestParcelModels:
    def test_parcel_item(self):
        data = require_fixture("ParcelItem", "GET", "/job/{id}/parcelitems")
        _validate_fixture(ParcelItem, data)

    def test_parcel_item_with_materials(self):
        data = require_fixture("ParcelItemWithMaterials", "GET", "/job/{id}/parcel-items-with-materials")
        _validate_fixture(ParcelItemWithMaterials, data)

    def test_packaging_container(self):
        data = require_fixture("PackagingContainer", "GET", "/job/{id}/packagingcontainers")
        _validate_fixture(PackagingContainer, data)
