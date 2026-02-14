"""Fixture validation tests for Catalog API models (T058)."""

import pytest

from tests.conftest import load_fixture

from ab.api.models.catalog import CatalogExpandedDto, CatalogWithSellersDto
from ab.api.models.lots import LotDataDto, LotDto, LotOverrideDto
from ab.api.models.sellers import SellerDto, SellerExpandedDto


class TestCatalogModels:
    @pytest.mark.mock
    def test_catalog_with_sellers_dto(self):
        data = load_fixture("CatalogWithSellersDto")
        model = CatalogWithSellersDto.model_validate(data)
        assert model.id is not None
        assert model.title is not None

    @pytest.mark.mock
    def test_catalog_expanded_dto(self):
        data = load_fixture("CatalogExpandedDto")
        model = CatalogExpandedDto.model_validate(data)
        assert model.id is not None
        assert model.title is not None

    @pytest.mark.mock
    def test_lot_dto(self):
        data = load_fixture("LotDto")
        model = LotDto.model_validate(data)
        assert model.id is not None

    @pytest.mark.mock
    def test_lot_data_dto(self):
        data = load_fixture("LotDataDto")
        model = LotDataDto.model_validate(data)
        assert isinstance(model.description, (str, type(None)))

    @pytest.mark.mock
    def test_lot_override_dto(self):
        data = load_fixture("LotOverrideDto")
        model = LotOverrideDto.model_validate(data)
        assert model.customer_item_id is not None

    @pytest.mark.mock
    def test_seller_dto(self):
        data = load_fixture("SellerDto")
        model = SellerDto.model_validate(data)
        assert model.id is not None
        assert model.name is not None

    @pytest.mark.live
    def test_seller_expanded_dto(self):
        data = load_fixture("SellerExpandedDto")
        model = SellerExpandedDto.model_validate(data)
        assert model.id is not None
