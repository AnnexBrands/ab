"""Live integration tests for Lots API."""

import pytest

from ab.api.models.lots import LotDto
from ab.api.models.shared import PaginatedList
from tests.conftest import assert_no_extra_fields
from tests.constants import LIVE_CATALOG_ID

pytestmark = pytest.mark.live


class TestLotsIntegration:
    def test_list_lots(self, api):
        result = api.lots.list()
        assert isinstance(result, PaginatedList)
        if len(result.items) > 0:
            assert isinstance(result.items[0], LotDto)
            assert_no_extra_fields(result.items[0])

    def test_get_lot(self, api):
        result = api.lots.get(LIVE_CATALOG_ID)
        if result is not None:
            assert isinstance(result, LotDto)
            assert_no_extra_fields(result)
