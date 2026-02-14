"""Fixture validation tests for Document models (T062)."""

import pytest

from tests.conftest import load_fixture

from ab.api.models.documents import Document


class TestDocumentModels:
    @pytest.mark.live
    def test_document(self):
        data = load_fixture("Document")
        model = Document.model_validate(data)
        assert model.id == 1771682
        assert model.file_name == "USAR(7).pdf"
        assert model.type_name == "USAR"
