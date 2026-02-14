"""Document models for the ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.mixins import IdentifiedModel


class Document(ResponseModel, IdentifiedModel):
    """Document record — GET /documents/list."""

    doc_path: Optional[str] = Field(None, alias="docPath", description="Document storage path")
    doc_type: Optional[int] = Field(None, alias="docType", description="Document type ID")
    file_name: Optional[str] = Field(None, alias="fileName", description="Original file name")
    sharing_level: Optional[int] = Field(None, alias="sharingLevel", description="Sharing level")


class DocumentUpdateRequest(RequestModel):
    """Body for PUT /documents/update/{docId}."""

    doc_type: Optional[int] = Field(None, alias="docType", description="Updated document type")
    sharing_level: Optional[int] = Field(None, alias="sharingLevel", description="Updated sharing level")
