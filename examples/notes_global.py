"""Example: Global note operations (4 methods).

Covers list, create, update, and suggest users.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Global Notes", env="staging")

TEST_NOTE_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# Notes CRUD
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list",
    lambda api: api.notes.list(),
    response_model="List[GlobalNote]",
    fixture_file="GlobalNote.json",
)

runner.add(
    "create",
    lambda api, data=None: api.notes.create(data=data or {}),
    request_model="GlobalNoteCreateRequest",
    request_fixture_file="GlobalNoteCreateRequest.json",
    response_model="GlobalNote",
    fixture_file="GlobalNote.json",
)

runner.add(
    "update",
    lambda api, data=None: api.notes.update(TEST_NOTE_ID, data=data or {}),
    request_model="GlobalNoteUpdateRequest",
    request_fixture_file="GlobalNoteUpdateRequest.json",
    response_model="GlobalNote",
    fixture_file="GlobalNote.json",
)

runner.add(
    "suggest_users",
    lambda api: api.notes.suggest_users(search_key="test"),
    response_model="List[SuggestedUser]",
    fixture_file="SuggestedUser.json",
)

if __name__ == "__main__":
    runner.run()
