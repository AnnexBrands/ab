# Documents

```{eval-rst}
.. autoclass:: ab.api.endpoints.documents.DocumentsEndpoint
   :members:
   :undoc-members:
```

## Methods

### upload

`POST /document/upload` — Upload a document (multipart).

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
result = api.documents.upload(job_id="...", file_path="/path/to/file.pdf")
```

### list

`GET /document/list` — List documents.

**Returns:** `list[`{class}`~ab.api.models.documents.Document`]`

```python
docs = api.documents.list(job_id="...")
```

### get

`GET /document/get` — Download a document (binary).

**Returns:** `bytes`

```python
content = api.documents.get("path/to/document.pdf")
with open("downloaded.pdf", "wb") as f:
    f.write(content)
```

### update

`PUT /document/update` — Update document metadata.

```python
api.documents.update("doc-id", {"sharingLevel": 1})
```
