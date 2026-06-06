"""Unit tests for the documents endpoint group.

These lock in the **wire-level behaviour** of the document upload methods
using a mocked :class:`~ab.http.HttpClient`:

* ``upload`` builds the swagger multipart form (PascalCase aliases) and
  streams the file as the ``file`` part,
* ``upload_item_photo`` is a thin wrapper that sets
  ``DocumentType.ITEM_PHOTO`` and routes item id(s) to ``JobItems``,
* ``upload_item_photos`` always returns a list — one result per file.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ab.api.endpoints.documents import DocumentsEndpoint
from ab.api.models.documents import DocumentUploadResponse
from ab.api.models.enums import DocumentType


@pytest.fixture
def client():
    c = MagicMock(name="HttpClient")
    c.request.return_value = {"success": True, "id": 999, "fileName": "x.jpg"}
    return c


@pytest.fixture
def documents(client):
    return DocumentsEndpoint(client)


@pytest.fixture
def photo(tmp_path):
    p = tmp_path / "photo.jpg"
    p.write_bytes(b"\xff\xd8jpeg-bytes")
    return p


def _last_call(client):
    args, kwargs = client.request.call_args
    return args, kwargs


def test_upload_builds_multipart_form(documents, client, photo):
    result = documents.upload(
        job_display_id="2000000",
        file_path=photo,
        document_type=DocumentType.BOL,
        shared=0,
    )
    args, kwargs = _last_call(client)
    assert args == ("POST", "/documents")
    # Form fields use the swagger PascalCase aliases; the enum serialises to int.
    assert kwargs["data"]["JobDisplayId"] == "2000000"
    assert kwargs["data"]["DocumentType"] == int(DocumentType.BOL)
    # exclude_none drops unset optional fields.
    assert "JobItems" not in kwargs["data"]
    # The file is streamed as the ``file`` multipart part.
    assert kwargs["files"]["file"][0] == "photo.jpg"
    assert isinstance(result, DocumentUploadResponse)
    assert result.success is True


def test_upload_item_photo_sets_type_and_items(documents, client, photo):
    documents.upload_item_photo(
        job_display_id="2000000",
        item_ids="ITEM-UUID-1",
        file_path=photo,
    )
    _args, kwargs = _last_call(client)
    data = kwargs["data"]
    assert data["DocumentType"] == int(DocumentType.ITEM_PHOTO) == 6
    assert data["DocumentTypeDescription"] == "Item Photo"
    # A single id is normalised to a one-element JobItems list.
    assert data["JobItems"] == ["ITEM-UUID-1"]


def test_upload_item_photo_accepts_id_list(documents, client, photo):
    documents.upload_item_photo(
        job_display_id="2000000",
        item_ids=["A", "B"],
        file_path=photo,
    )
    _args, kwargs = _last_call(client)
    assert kwargs["data"]["JobItems"] == ["A", "B"]


def test_upload_item_photos_returns_one_result_per_file(documents, client, tmp_path):
    files = []
    for i in range(3):
        p = tmp_path / f"p{i}.jpg"
        p.write_bytes(b"\xff\xd8")
        files.append(p)

    results = documents.upload_item_photos(
        job_display_id="2000000",
        item_ids="ITEM-UUID-1",
        file_paths=files,
    )
    assert isinstance(results, list)
    assert len(results) == 3
    assert all(isinstance(r, DocumentUploadResponse) for r in results)
    assert client.request.call_count == 3


def test_upload_item_photos_single_file_still_returns_list(documents, client, photo):
    """Regression vs the legacy SDK's variable return — always a list."""
    results = documents.upload_item_photos(
        job_display_id="2000000",
        item_ids="ITEM-UUID-1",
        file_paths=[photo],
    )
    assert isinstance(results, list)
    assert len(results) == 1


@pytest.mark.parametrize("bad_item_ids", [[], "", "   ", ["A", ""], [" "]])
def test_upload_item_photo_rejects_empty_item_ids(documents, client, photo, bad_item_ids):
    """The 'one or more job items' contract is enforced, not silently sent as JobItems=[]."""
    with pytest.raises(ValueError, match="item_ids"):
        documents.upload_item_photo(
            job_display_id="2000000",
            item_ids=bad_item_ids,
            file_path=photo,
        )
    client.request.assert_not_called()
