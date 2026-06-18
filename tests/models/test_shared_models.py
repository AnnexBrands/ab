"""Fixture validation tests for ServiceBaseResponse."""

from ab.api.models.shared import BookedDocument, ServiceBaseResponse
from ab.api.models.shipments import ShipmentWeight
from tests.conftest import assert_no_extra_fields, require_fixture


class TestServiceBaseResponse:
    def test_service_base_response(self):
        """Validate fixture against expanded model — zero extra fields."""
        data = require_fixture("ServiceBaseResponse", "POST", "/job/{id}/shipment/book")
        model = ServiceBaseResponse.model_validate(data)
        assert isinstance(model, ServiceBaseResponse)
        assert_no_extra_fields(model)

    def test_service_base_response_fields(self):
        """Verify key fields are populated in the captured fixture."""
        data = require_fixture("ServiceBaseResponse", "POST", "/job/{id}/shipment/book")
        model = ServiceBaseResponse.model_validate(data)
        assert model.success is not None
        assert model.documents is not None
        assert model.weight is not None

    def test_weight_nested_model(self):
        """Verify nested ShipmentWeight is parsed as a typed model."""
        data = require_fixture("ServiceBaseResponse", "POST", "/job/{id}/shipment/book")
        model = ServiceBaseResponse.model_validate(data)
        assert model.weight is not None
        assert isinstance(model.weight, ShipmentWeight)
        assert_no_extra_fields(model.weight)

    def test_documents_accepts_object_documents(self):
        """A successful book returns document OBJECTS (label byte codes), not just
        strings. Regression for the live ValidationError on job 7036373's book —
        ``documents`` was typed ``list[str]`` so the success envelope crashed.
        """
        data = {
            "success": True,
            "shipmentId": "abc-123",
            "documents": [{"documentId": 99, "docType": "Label", "byteCode": "JVBERi0x"}],
        }
        model = ServiceBaseResponse.model_validate(data)
        assert model.success is True
        assert len(model.documents) == 1
        doc = model.documents[0]
        assert isinstance(doc, BookedDocument)
        assert doc.byte_code == "JVBERi0x"
        assert doc.doc_type == "Label"

    def test_documents_still_accepts_string_documents(self):
        """Backward compatibility: operations that return document URL/reference
        strings must keep validating after the object-document fix.
        """
        model = ServiceBaseResponse.model_validate({"success": True, "documents": ["https://x/doc.pdf"]})
        assert model.documents == ["https://x/doc.pdf"]
