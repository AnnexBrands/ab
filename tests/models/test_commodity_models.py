"""Fixture validation tests for Commodity models."""

from ab.api.models.commodities import Commodity, CommodityMap
from tests.conftest import require_fixture


class TestCommodityModels:
    def test_commodity(self):
        data = require_fixture("Commodity", "POST", "/commodity/search")
        Commodity.model_validate(data)

    def test_commodity_map(self):
        data = require_fixture("CommodityMap", "POST", "/commodity-map/search")
        CommodityMap.model_validate(data)
