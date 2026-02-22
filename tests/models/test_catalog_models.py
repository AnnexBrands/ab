"""Fixture validation tests for Catalog API models."""

import pytest

from ab.api.models.catalog import CatalogExpandedDto, CatalogWithSellersDto
from ab.api.models.lots import LotDataDto, LotDto, LotOverrideDto
from ab.api.models.sellers import SellerDto, SellerExpandedDto
from tests.conftest import assert_no_extra_fields, require_fixture


class TestCatalogModels:
    def test_catalog_with_sellers_dto(self):
        data = require_fixture("CatalogWithSellersDto", "GET", "/Catalog")
        model = CatalogWithSellersDto.model_validate(data)
        assert isinstance(model, CatalogWithSellersDto)
        assert_no_extra_fields(model)

    def test_catalog_expanded_dto(self):
        data = require_fixture("CatalogExpandedDto", "GET", "/Catalog/{id}")
        model = CatalogExpandedDto.model_validate(data)
        assert isinstance(model, CatalogExpandedDto)
        assert_no_extra_fields(model)

    def test_lot_dto(self):
        data = require_fixture("LotDto", "GET", "/Lot")
        model = LotDto.model_validate(data)
        assert isinstance(model, LotDto)
        assert_no_extra_fields(model)

    def test_lot_data_dto(self):
        data = require_fixture("LotDataDto", "GET", "/Lot/{id}")
        model = LotDataDto.model_validate(data)
        assert isinstance(model, LotDataDto)
        assert_no_extra_fields(model)

    def test_lot_override_dto(self):
        data = require_fixture("LotOverrideDto", "POST", "/Lot/overrides")
        model = LotOverrideDto.model_validate(data)
        assert isinstance(model, LotOverrideDto)
        assert_no_extra_fields(model)

    @pytest.mark.live
    def test_seller_dto(self):
        data = require_fixture("SellerDto", "GET", "/Seller/{id}", required=True)
        model = SellerDto.model_validate(data)
        assert isinstance(model, SellerDto)
        assert_no_extra_fields(model)

    @pytest.mark.live
    def test_seller_expanded_dto(self):
        data = require_fixture("SellerExpandedDto", "GET", "/Seller/{id}", required=True)
        # Fixture may be a paginated wrapper {items, pageNumber, ...}
        if isinstance(data, dict) and "items" in data:
            items = data["items"]
            assert len(items) > 0, "SellerExpandedDto fixture has empty items array"
            data = items[0]
        model = SellerExpandedDto.model_validate(data)
        assert isinstance(model, SellerExpandedDto)
        assert_no_extra_fields(model)
