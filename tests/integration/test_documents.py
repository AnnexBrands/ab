"""Live integration tests for Documents API (T073)."""

import pytest

pytestmark = pytest.mark.live


class TestDocumentsIntegration:
    def test_list_documents(self, api):
        result = api.documents.list()
        assert result is not None
