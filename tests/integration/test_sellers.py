"""Live integration tests for Sellers API (T078)."""

import pytest

from tests.constants import LIVE_SELLER_ID

pytestmark = pytest.mark.live


class TestSellersIntegration:
    def test_list_sellers(self, api):
        result = api.sellers.list()
        assert result is not None

    def test_get_seller(self, api):
        result = api.sellers.get(LIVE_SELLER_ID)
        assert result is not None
