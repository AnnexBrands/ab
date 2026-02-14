"""Example: Document operations (4 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Documents", env="staging")

LIVE_JOB_DISPLAY_ID = 2000000

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "list",
    lambda api: api.documents.list(job_id="2000000"),
    response_model="List[Document]",
    fixture_file="Document.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "upload",
    lambda api: api.documents.upload(
        # TODO: capture fixture — needs valid job ID and local file path
        job_id="2000000",
        file_path="/tmp/test-upload.pdf",
        document_type=6,
        sharing_level=0,
    ),
)

runner.add(
    "get",
    lambda api: api.documents.get(
        # TODO: capture fixture — needs valid document path from list response
        #       binary response — fixture save N/A
        "path/to/document.pdf",
    ),
)

runner.add(
    "update",
    lambda api: api.documents.update(
        # TODO: capture fixture — needs valid document ID and DocumentUpdateRequest body
        "doc-id-placeholder",
        {},
    ),
    request_model="DocumentUpdateRequest",
)

if __name__ == "__main__":
    runner.run()
