"""Example: Document operations (4 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Documents", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "list",
    lambda api: api.documents.list(job_display_id="2000000"),
    response_model="List[Document]",
    fixture_file="Document.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "upload",
    lambda api: api.documents.upload(
        job_id="2000000",
        file_path="/tmp/test-upload.pdf",
        document_type=6,
        sharing_level=0,
    ),
)

runner.add(
    "get",
    lambda api: api.documents.get("path/to/document.pdf"),
)

runner.add(
    "update",
    lambda api, data=None: api.documents.update("doc-id-placeholder", data=data or {}),
    request_model="DocumentUpdateRequest",
    request_fixture_file="DocumentUpdateRequest.json",
)

if __name__ == "__main__":
    runner.run()
