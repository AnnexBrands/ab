"""Example: Global note operations (4 methods).

Covers list, create, update, and suggest users.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Global Notes", env="staging")

LIVE_NOTE_ID = "PLACEHOLDER"

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
    lambda api: api.notes.create(comment="Test note from SDK", category="General"),
    request_model="GlobalNoteCreateRequest",
    response_model="GlobalNote",
)

runner.add(
    "update",
    lambda api: api.notes.update(LIVE_NOTE_ID, comment="Updated note"),
    request_model="GlobalNoteUpdateRequest",
    response_model="GlobalNote",
)

runner.add(
    "suggest_users",
    lambda api: api.notes.suggest_users(),
    response_model="List[SuggestedUser]",
    fixture_file="SuggestedUser.json",
)

if __name__ == "__main__":
    runner.run()
