"""Live integration tests for Catalog API."""

import pytest

from ab.api.models.catalog import CatalogExpandedDto
from ab.api.models.shared import PaginatedList
from tests.conftest import assert_no_extra_fields
from tests.constants import TEST_CATALOG_ID

pytestmark = pytest.mark.live


class TestCatalogIntegration:
    def test_list_catalogs(self, api):
        result = api.catalog.list()
        assert isinstance(result, PaginatedList)
        if len(result.items) > 0:
            assert isinstance(result.items[0], CatalogExpandedDto)
            assert_no_extra_fields(result.items[0])

    def test_get_catalog(self, api):
        result = api.catalog.get(TEST_CATALOG_ID)
        # May return None if no catalog data in staging
        if result is not None:
            assert isinstance(result, CatalogExpandedDto)
            assert_no_extra_fields(result)
