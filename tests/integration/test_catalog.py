"""Live integration tests for Catalog API (T069)."""

import pytest

pytestmark = pytest.mark.live


class TestCatalogIntegration:
    def test_list_catalogs(self, api):
        result = api.catalog.list()
        assert result is not None

    def test_get_catalog(self, api):
        from tests.constants import LIVE_CATALOG_ID

        result = api.catalog.get(LIVE_CATALOG_ID)
        # May return None if no catalog data in staging
        if result is not None:
            assert hasattr(result, "id") or hasattr(result, "name")
