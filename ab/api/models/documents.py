"""Document models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.mixins import IdentifiedModel


class DocumentListParams(RequestModel):
    """Query parameters for GET /documents/list."""

    job_display_id: Optional[str] = Field(None, alias="jobDisplayId", description="Job display identifier")


class Document(ResponseModel, IdentifiedModel):
    """Document record — GET /documents/list and embedded in Job response.

    Live API field names differ from swagger: ``path`` not ``docPath``,
    ``typeName`` not ``docType``, ``shared`` not ``sharingLevel``.
    """

    path: Optional[str] = Field(None, description="Document storage path")
    thumbnail_path: Optional[str] = Field(None, alias="thumbnailPath", description="Thumbnail path")
    description: Optional[str] = Field(None, description="Document description")
    type_name: Optional[str] = Field(None, alias="typeName", description="Document type name")
    type_id: Optional[int] = Field(None, alias="typeId", description="Document type ID")
    file_name: Optional[str] = Field(None, alias="fileName", description="Original file name")
    shared: Optional[int] = Field(None, description="Sharing level (0=private)")
    tags: Optional[List] = Field(None, description="Document tags")
    job_items: Optional[List] = Field(None, alias="jobItems", description="Associated job items")


class DocumentUpdateRequest(RequestModel):
    """Body for PUT /documents/update/{docId}."""

    doc_type: Optional[int] = Field(None, alias="docType", description="Updated document type")
    sharing_level: Optional[int] = Field(None, alias="sharingLevel", description="Updated sharing level")
