"""Documents API endpoints."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ab.api.base import BaseEndpoint
from ab.api.models.documents import DocumentUploadRequest, DocumentUploadResponse
from ab.api.models.enums import DocumentType
from ab.api.route import Route

if TYPE_CHECKING:
    from ab.api.models.documents import Document, DocumentUpdateRequest

_UPLOAD = Route(
    "POST", "/documents",
    request_model="DocumentUploadRequest", response_model="DocumentUploadResponse",
)
_LIST = Route("GET", "/documents/list", params_model="DocumentListParams", response_model="List[Document]")
_GET = Route("GET", "/documents/get/{docPath}", response_model="bytes")
_UPDATE = Route("PUT", "/documents/update/{docId}", request_model="DocumentUpdateRequest")


class DocumentsEndpoint(BaseEndpoint):
    """Operations on documents (ACPortal API)."""

    def upload(
        self,
        *,
        job_display_id: str,
        file_path: str | Path,
        document_type: DocumentType | int,
        document_type_description: str | None = None,
        shared: int = 0,
        tags: list[str] | None = None,
        job_items: list[str] | None = None,
        rfq_id: int | None = None,
        filename: str | None = None,
    ) -> DocumentUploadResponse:
        """POST /documents — upload a single document of any type (multipart).

        The accompanying form fields are validated through
        :class:`~ab.api.models.documents.DocumentUploadRequest` and the file is
        streamed as the ``file`` part. This is the canonical upload primitive;
        :meth:`upload_item_photo` is a thin wrapper that fills in the
        item-photo specifics.

        Args:
            job_display_id: Job display ID the document belongs to.
            file_path: Path to the file to upload.
            document_type: Document type; see :class:`~ab.api.models.enums.DocumentType`.
            document_type_description: Optional human-readable type label.
            shared: Sharing bitmask (0 = private).
            tags: Optional tags to attach.
            job_items: Item UUID(s) to associate (used for item photos).
            rfq_id: Optional RFQ ID to associate.
            filename: Override the multipart filename (defaults to the file's name).

        Returns:
            DocumentUploadResponse: The parsed upload result.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/documents/upload.html
        Request model: DocumentUploadRequest
        Response model: DocumentUploadResponse
        """
        form = DocumentUploadRequest(
            job_display_id=job_display_id,
            document_type=document_type,
            document_type_description=document_type_description,
            shared=shared,
            tags=tags,
            job_items=job_items,
            rfq_id=rfq_id,
        )
        data = form.model_dump(by_alias=True, exclude_none=True)
        path = Path(file_path)
        with open(path, "rb") as fh:
            files = {"file": (filename or path.name, fh, "application/octet-stream")}
            return self._request(_UPLOAD, files=files, data=data)

    def upload_item_photo(
        self,
        *,
        job_display_id: str,
        item_ids: str | list[str],
        file_path: str | Path,
        shared: int = 0,
        tags: list[str] | None = None,
        filename: str | None = None,
    ) -> DocumentUploadResponse:
        """Upload one item photo, associated with one or more job items.

        A thin convenience wrapper over :meth:`upload` that sets
        ``document_type=DocumentType.ITEM_PHOTO`` and routes ``item_ids`` to the
        ``JobItems`` form field. Accepts a single item UUID or a list.

        Args:
            job_display_id: Job display ID the photo belongs to.
            item_ids: One item UUID, or a list of UUIDs, to attach the photo to.
            file_path: Path to the image file.
            shared: Sharing bitmask (0 = private).
            tags: Optional tags to attach.
            filename: Override the multipart filename (defaults to the file's name).

        Returns:
            DocumentUploadResponse: The parsed upload result.
        """
        items = [item_ids] if isinstance(item_ids, str) else list(item_ids)
        if not items or any(not str(i).strip() for i in items):
            raise ValueError("item_ids must contain one or more non-empty item id(s)")
        return self.upload(
            job_display_id=job_display_id,
            file_path=file_path,
            document_type=DocumentType.ITEM_PHOTO,
            document_type_description="Item Photo",
            shared=shared,
            tags=tags,
            job_items=items,
            filename=filename,
        )

    def upload_item_photos(
        self,
        *,
        job_display_id: str,
        item_ids: str | list[str],
        file_paths: list[str | Path],
        shared: int = 0,
        tags: list[str] | None = None,
    ) -> list[DocumentUploadResponse]:
        """Upload several item photos in one call — one request per file.

        Returns one :class:`~ab.api.models.documents.DocumentUploadResponse`
        per file, in the same order as ``file_paths`` (always a list, even for
        a single file — unlike the legacy SDK's variable return). Every file is
        attached to the same ``item_ids``.

        Args:
            job_display_id: Job display ID the photos belong to.
            item_ids: One item UUID, or a list of UUIDs, to attach every photo to.
            file_paths: Paths to the image files to upload.
            shared: Sharing bitmask (0 = private).
            tags: Optional tags to attach to every photo.

        Returns:
            list[DocumentUploadResponse]: One result per uploaded file, in order.
        """
        return [
            self.upload_item_photo(
                job_display_id=job_display_id,
                item_ids=item_ids,
                file_path=file_path,
                shared=shared,
                tags=tags,
            )
            for file_path in file_paths
        ]

    def list(self, job_display_id: str | int) -> list[Document]:
        """GET /documents/list

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/documents/list.html
        Query params: DocumentListParams
        Response model: List[Document]
        """
        return self._request(_LIST, params=dict(job_display_id=str(job_display_id)))

    def get(self, doc_path: str) -> bytes:
        """GET /documents/get/{docPath} — returns raw bytes."""
        return self._client.request("GET", f"/documents/get/{doc_path}", raw=True).content

    def update(self, doc_id: str, *, data: DocumentUpdateRequest | dict) -> None:
        """PUT /documents/update/{docId}.

        Args:
            doc_id: Document identifier.
            data: Document update payload.
                Accepts a :class:`DocumentUpdateRequest` instance or a dict.

        Request model: :class:`DocumentUpdateRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/documents/update.html
        Request model: DocumentUpdateRequest
        """
        return self._request(_UPDATE.bind(docId=doc_id), json=data)
