"""Fixture validation tests for Document models (T062)."""

import pytest

from tests.conftest import load_fixture

from ab.api.models.documents import Document


class TestDocumentModels:
    @pytest.mark.mock
    def test_document(self):
        data = load_fixture("Document")
        model = Document.model_validate(data)
