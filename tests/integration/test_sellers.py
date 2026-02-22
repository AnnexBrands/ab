"""Live integration tests for Sellers API."""

import pytest

from ab.api.models.sellers import SellerExpandedDto
from ab.api.models.shared import PaginatedList
from tests.conftest import assert_no_extra_fields
from tests.constants import LIVE_SELLER_ID

pytestmark = pytest.mark.live


class TestSellersIntegration:
    def test_list_sellers(self, api):
        result = api.sellers.list()
        assert isinstance(result, PaginatedList)
        assert len(result.items) > 0
        assert isinstance(result.items[0], SellerExpandedDto)
        assert_no_extra_fields(result.items[0])

    def test_get_seller(self, api):
        result = api.sellers.get(LIVE_SELLER_ID)
        assert isinstance(result, SellerExpandedDto)
        assert_no_extra_fields(result)
