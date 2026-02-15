"""Fixture validation tests for Commodity models."""

from tests.conftest import require_fixture

from ab.api.models.commodities import Commodity, CommodityMap


class TestCommodityModels:
    def test_commodity(self):
        data = require_fixture("Commodity", "POST", "/commodity/search")
        model = Commodity.model_validate(data)

    def test_commodity_map(self):
        data = require_fixture("CommodityMap", "POST", "/commodity-map/search")
        model = CommodityMap.model_validate(data)
