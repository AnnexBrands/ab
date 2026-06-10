"""Example: Document operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (``examples/_documents.py``) to the plain-script form.

See also: https://ab-sdk.readthedocs.io/en/latest/api/documents.html
"""

from __future__ import annotations

from pathlib import Path

from ab import ABConnectAPI
from ab.api.models.enums import DocumentType
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /documents/list
    print(f"\n# api.documents.list(job_display_id={TEST_JOB_DISPLAY_ID!r})")
    result = api.documents.list(job_display_id=TEST_JOB_DISPLAY_ID)
    print(format_result(result))
    save("Document.json", result)

    # GET /documents/get/{docPath} — download the first listed document (bytes).
    docs_with_path = [d for d in result if d.path]
    if docs_with_path:
        doc = docs_with_path[0]
        print(f"\n# api.documents.get({doc.path!r})")
        content = api.documents.get(doc.path)
        print(f"  ({len(content)} bytes)")

        # GET /documents/get/thumbnail/{docPath} — thumbnail bytes.
        print(f"\n# api.documents.get_thumbnail({doc.path!r})")
        thumb = api.documents.get_thumbnail(doc.path)
        print(f"  ({len(thumb)} bytes)")
    else:
        print("\n# api.documents.get / get_thumbnail skipped — job has no documents with a path")

    # PUT /documents/hide/{docId} — hides the document from listings (mutates staging).
    if mutations_enabled() and docs_with_path:
        doc_id = docs_with_path[0].id
        print(f"\n# api.documents.hide({doc_id!r})")
        api.documents.hide(doc_id)
        print("  (hidden)")
    else:
        print("\n# api.documents.hide skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # POST /documents — upload a single document (multipart, mutates staging).
    if mutations_enabled():
        upload_path = Path("/tmp/test-upload.pdf")
        upload_path.write_bytes(b"%PDF-1.4 example upload\n")
        print(
            f"\n# api.documents.upload(job_display_id={TEST_JOB_DISPLAY_ID!r}, "
            f"file_path={str(upload_path)!r}, document_type=DocumentType.BOL)"
        )
        result = api.documents.upload(
            job_display_id=str(TEST_JOB_DISPLAY_ID),
            file_path=str(upload_path),
            document_type=DocumentType.BOL,
        )
        print(format_result(result))
        save("mocks/DocumentUploadResponse.json", result)
    else:
        print("\n# api.documents.upload skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # PUT /documents/update/{docId} — mutates staging.
    if mutations_enabled():
        doc_id = "doc-id-placeholder"  # supply a real document id from api.documents.list
        print(f"\n# api.documents.update({doc_id!r}, data=DocumentUpdateRequest(...))")
        result = api.documents.update(doc_id, data=load_request("DocumentUpdateRequest.json"))
        print(format_result(result))
    else:
        print("\n# api.documents.update skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
