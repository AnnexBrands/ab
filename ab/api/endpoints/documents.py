"""Documents API endpoints (6 routes)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_UPLOAD = Route("POST", "/documents")
_LIST = Route("GET", "/documents/list", response_model="List[Document]")
_GET = Route("GET", "/documents/get/{docPath}", response_model="bytes")
_UPDATE = Route("PUT", "/documents/update/{docId}", request_model="DocumentUpdateRequest")


# Extended document routes (009)
_GET_THUMBNAIL = Route("GET", "/documents/get/thumbnail/{docPath}", response_model="bytes")
_PUT_HIDE = Route("PUT", "/documents/hide/{docId}")


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

    def list(self, *, job_display_id: Optional[str] = None, **params: Any) -> Any:
        """GET /documents/list"""
        if job_display_id:
            params["jobDisplayId"] = job_display_id
        return self._request(_LIST, params=params)

    def get(self, doc_path: str) -> bytes:
        """GET /documents/get/{docPath} — returns raw bytes."""
        return self._client.request("GET", f"/documents/get/{doc_path}", raw=True).content

    def update(self, doc_id: str, data: dict | Any) -> Any:
        """PUT /documents/update/{docId}"""
        return self._request(_UPDATE.bind(docId=doc_id), json=data)

    # ---- Extended (009) -----------------------------------------------------

    def get_thumbnail(self, doc_path: str) -> bytes:
        """GET /documents/get/thumbnail/{docPath} — returns raw bytes."""
        return self._client.request("GET", f"/documents/get/thumbnail/{doc_path}", raw=True).content

    def hide(self, doc_id: str) -> Any:
        """PUT /documents/hide/{docId}"""
        return self._request(_PUT_HIDE.bind(docId=doc_id))
