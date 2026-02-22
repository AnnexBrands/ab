"""Live integration tests for Documents API."""

import pytest

from ab.api.models.documents import Document
from tests.conftest import assert_no_extra_fields

pytestmark = pytest.mark.live


class TestDocumentsIntegration:
    def test_list_documents(self, api):
        result = api.documents.list()
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], Document)
        assert_no_extra_fields(result[0])
