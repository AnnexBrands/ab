"""Live integration tests for Lots API (T077)."""

import pytest

pytestmark = pytest.mark.live


class TestLotsIntegration:
    def test_list_lots(self, api):
        result = api.lots.list()
        assert result is not None

    def test_get_lot(self, api):
        from tests.constants import LIVE_CATALOG_ID

        # Lots are tied to catalogs; may be empty in staging
        result = api.lots.get(LIVE_CATALOG_ID)
        if result is not None:
            assert hasattr(result, "id") or isinstance(result, dict)
