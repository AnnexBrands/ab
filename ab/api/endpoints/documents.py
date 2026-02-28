"""Documents API endpoints (4 routes)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ab.api.models.documents import Document

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_UPLOAD = Route("POST", "/documents")
_LIST = Route("GET", "/documents/list", params_model="DocumentListParams", response_model="List[Document]")
_GET = Route("GET", "/documents/get/{docPath}", response_model="bytes")
_UPDATE = Route("PUT", "/documents/update/{docId}", request_model="DocumentUpdateRequest")


class DocumentsEndpoint(BaseEndpoint):
    """Operations on documents (ACPortal API)."""

    def upload(self, *, job_id: str, file_path: str, document_type: int = 6, sharing_level: int = 0) -> Any:
        """POST /documents — multipart file upload."""
        p = Path(file_path)
        with open(p, "rb") as f:
            files = {"file": (p.name, f, "application/octet-stream")}
            data = {
                "jobId": job_id,
                "documentType": str(document_type),
                "sharingLevel": str(sharing_level),
            }
            return self._client.request("POST", "/documents", files=files, data=data)

    def list(self, job_display_id: str | int) -> list[Document]:
        """GET /documents/list"""
        return self._request(_LIST, params=dict(job_display_id=str(job_display_id)))

    def get(self, doc_path: str) -> bytes:
        """GET /documents/get/{docPath} — returns raw bytes."""
        return self._client.request("GET", f"/documents/get/{doc_path}", raw=True).content

    def update(
        self,
        doc_id: str,
        *,
        doc_type: int | None = None,
        sharing_level: int | None = None,
    ) -> Any:
        """PUT /documents/update/{docId}.

        Args:
            doc_id: Document identifier.
            doc_type: Updated document type.
            sharing_level: Updated sharing level.

        Request model: :class:`DocumentUpdateRequest`
        """
        body = dict(doc_type=doc_type, sharing_level=sharing_level)
        return self._request(_UPDATE.bind(docId=doc_id), json=body)
