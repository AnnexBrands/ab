"""Fixture validation tests for Commodity models."""

from ab.api.models.commodities import Commodity, CommodityMap
from tests.conftest import assert_no_extra_fields, require_fixture


class TestCommodityModels:
    def test_commodity(self):
        data = require_fixture("Commodity", "POST", "/commodity/search")
        model = Commodity.model_validate(data)
        assert isinstance(model, Commodity)
        assert_no_extra_fields(model)

    def test_commodity_map(self):
        data = require_fixture("CommodityMap", "POST", "/commodity-map/search")
        model = CommodityMap.model_validate(data)
        assert isinstance(model, CommodityMap)
        assert_no_extra_fields(model)
