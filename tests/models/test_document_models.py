"""Fixture validation tests for Document models."""

import pytest

from ab.api.models.documents import Document
from tests.conftest import assert_no_extra_fields, require_fixture


class TestDocumentModels:
    @pytest.mark.live
    def test_document(self):
        data = require_fixture("Document", "GET", "/documents", required=True)
        model = Document.model_validate(data)
        assert isinstance(model, Document)
        assert_no_extra_fields(model)
