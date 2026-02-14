"""Fixture validation tests for Document models (T062)."""

import pytest

from tests.conftest import require_fixture

from ab.api.models.documents import Document


class TestDocumentModels:
    @pytest.mark.live
    def test_document(self):
        data = require_fixture("Document", "GET", "/documents", required=True)
        model = Document.model_validate(data)
        assert model.id == 1771682
        assert model.file_name == "USAR(7).pdf"
        assert model.type_name == "USAR"
