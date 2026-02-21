"""Fixture validation tests for Catalog API models (T058)."""

import pytest

from ab.api.models.catalog import CatalogExpandedDto, CatalogWithSellersDto
from ab.api.models.lots import LotDataDto, LotDto, LotOverrideDto
from ab.api.models.sellers import SellerDto, SellerExpandedDto
from tests.conftest import require_fixture


class TestCatalogModels:
    def test_catalog_with_sellers_dto(self):
        data = require_fixture("CatalogWithSellersDto", "GET", "/Catalog")
        model = CatalogWithSellersDto.model_validate(data)
        assert model.id is not None
        assert model.title is not None

    def test_catalog_expanded_dto(self):
        data = require_fixture("CatalogExpandedDto", "GET", "/Catalog/{id}")
        model = CatalogExpandedDto.model_validate(data)
        assert model.id is not None
        assert model.title is not None

    def test_lot_dto(self):
        data = require_fixture("LotDto", "GET", "/Lot")
        model = LotDto.model_validate(data)
        assert model.id is not None

    def test_lot_data_dto(self):
        data = require_fixture("LotDataDto", "GET", "/Lot/{id}")
        model = LotDataDto.model_validate(data)
        assert isinstance(model.description, (str, type(None)))

    def test_lot_override_dto(self):
        data = require_fixture("LotOverrideDto", "POST", "/Lot/overrides")
        model = LotOverrideDto.model_validate(data)
        assert model.customer_item_id is not None

    @pytest.mark.live
    def test_seller_dto(self):
        data = require_fixture("SellerDto", "GET", "/Seller/{id}", required=True)
        model = SellerDto.model_validate(data)
        assert model.id is not None
        assert model.name is not None

    @pytest.mark.live
    def test_seller_expanded_dto(self):
        data = require_fixture("SellerExpandedDto", "GET", "/Seller/{id}", required=True)
        model = SellerExpandedDto.model_validate(data)
        assert model.id is not None
