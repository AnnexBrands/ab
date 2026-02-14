"""Example: Document operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# List documents
docs = api.documents.list()
print(f"Documents: {docs}")

# Upload a document (uncomment to run)
# result = api.documents.upload(job_id="...", file_path="/path/to/file.pdf")
# print(f"Uploaded: {result}")

# Download a document (uncomment to run)
# content = api.documents.get("path/to/document.pdf")
# with open("downloaded.pdf", "wb") as f:
#     f.write(content)
