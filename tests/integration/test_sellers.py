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
        # Fetch a valid seller ID from the list (staging data may change)
        listing = api.sellers.list()
        assert len(listing.items) > 0, "No sellers available on staging"
        seller_id = listing.items[0].id
        result = api.sellers.get(seller_id)
        assert isinstance(result, SellerExpandedDto)
        assert_no_extra_fields(result)
