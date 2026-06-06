"""Fixture validation tests for Document models."""

import json
from pathlib import Path

import pytest

from ab.api.models.documents import (
    Document,
    DocumentUploadRequest,
    DocumentUploadResponse,
    UploadedFile,
)
from ab.api.models.enums import DocumentType
from tests.conftest import assert_no_extra_fields, require_fixture

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class TestDocumentModels:
    @pytest.mark.live
    def test_document(self):
        data = require_fixture("Document", "GET", "/documents", required=True)
        model = Document.model_validate(data)
        assert isinstance(model, Document)
        assert_no_extra_fields(model)

    def test_document_upload_response(self):
        """The upload response model declares every field in its mock fixture
        (zero ``__pydantic_extra__``) — this is the G1/G3 evidence for the
        ``POST /documents`` route now that it carries a response model."""
        data = json.loads((FIXTURES / "mocks" / "DocumentUploadResponse.json").read_text())
        model = DocumentUploadResponse.model_validate(data)
        assert isinstance(model, DocumentUploadResponse)
        assert_no_extra_fields(model)
        assert all(isinstance(f, UploadedFile) for f in (model.uploaded_files or []))

    def test_document_upload_request_round_trips(self):
        """The request fixture validates and survives a serialize→validate round-trip."""
        data = json.loads((FIXTURES / "requests" / "DocumentUploadRequest.json").read_text())
        model = DocumentUploadRequest.model_validate(data)
        assert isinstance(model, DocumentUploadRequest)
        dumped = model.model_dump(by_alias=True, exclude_none=True, mode="json")
        # Item photos serialize DocumentType to its int value and JobItems as a list.
        assert dumped["DocumentType"] == int(DocumentType.ITEM_PHOTO)
        assert isinstance(dumped["JobItems"], list)
        assert isinstance(DocumentUploadRequest.model_validate(dumped), DocumentUploadRequest)


def test_document_type_enum_matches_lookup():
    """DocumentType values must mirror the live /lookup/documentTypes lookup.

    Guards against the enum silently drifting from swagger-truth again (its
    pre-correction values were wrong, e.g. labelling 6 as ``OTHER``).
    """
    rows = json.loads((FIXTURES / "DocumentTypeBySource.json").read_text())
    lookup_values = {row["value"] for row in rows}
    enum_values = {int(m) for m in DocumentType}
    assert enum_values == lookup_values, (
        "DocumentType drifted from the lookup: "
        f"only-in-enum={sorted(enum_values - lookup_values)}, "
        f"only-in-lookup={sorted(lookup_values - enum_values)}"
    )
    # Spot-check the member this feature depends on.
    assert int(DocumentType.ITEM_PHOTO) == 6
