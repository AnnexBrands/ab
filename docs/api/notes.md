# Notes

```{eval-rst}
.. autoclass:: ab.api.endpoints.notes.NotesEndpoint
   :members:
   :undoc-members:
```

## Methods

### list

`GET /note` — List global notes with optional filters.

**Returns:** `list[`{class}`~ab.api.models.notes.GlobalNote`]`

```python
# List all notes
notes = api.notes.list()

# Filter by job
notes = api.notes.list(jobId="job-uuid")
```

### create / update

`POST /note` / `PUT /note/{id}` — Create and update notes.

**Returns:** {class}`~ab.api.models.notes.GlobalNote`

```python
note = api.notes.create(comment="New note", category="General")
api.notes.update("note-id", comment="Updated")
```

### suggest_users

`GET /note/suggestUsers` — User suggestions for mentions.

**Returns:** `list[`{class}`~ab.api.models.notes.SuggestedUser`]`
