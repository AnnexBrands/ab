"""Global note models for the ACPortal API.

Source-of-truth schemas in swagger:

* ``Notes`` — response shape for ``GET /note``.
* ``NoteModel`` — request body for **both** ``POST /note`` and
  ``PUT /note/{id}``. The API does not split create-vs-update into two
  shapes; the SDK exposes a single :class:`NoteRequest` to match.
* ``SuggestedContactEntity`` — response item for ``GET /note/suggestUsers``.

The legacy ``GlobalNoteCreateRequest`` / ``GlobalNoteUpdateRequest`` names
remain as aliases for :class:`NoteRequest` so existing imports keep working.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel

# ---------------------------------------------------------------------------
# Query-parameter models
# ---------------------------------------------------------------------------


class NotesListParams(RequestModel):
    """Query parameters for GET /note."""

    category: Optional[List[str]] = Field(None, description="Filter by category UUIDs")
    job_id: Optional[str] = Field(None, alias="jobId", description="Filter by job UUID")
    contact_id: Optional[int] = Field(None, alias="contactId", description="Filter by contact ID")
    company_id: Optional[str] = Field(None, alias="companyId", description="Filter by company UUID")


class NotesSuggestUsersParams(RequestModel):
    """Query parameters for GET /note/suggestUsers.

    Swagger marks ``SearchKey`` as required. The endpoint method signature
    enforces this with a keyword-only required parameter so users can't
    accidentally omit it.
    """

    search_key: Optional[str] = Field(None, alias="SearchKey", description="User search keyword (required)")
    job_franchisee_id: Optional[str] = Field(
        None, alias="JobFranchiseeId", description="Job franchisee UUID"
    )
    company_id: Optional[str] = Field(None, alias="CompanyId", description="Company UUID filter")


# ---------------------------------------------------------------------------
# Suggested-user item
# ---------------------------------------------------------------------------


class SuggestedUser(ResponseModel):
    """User suggestion for mentions — element of ``GET /note/suggestUsers``.

    Shape matches swagger ``SuggestedContactEntity`` (``id``, ``fullName``).
    The ``id`` is the forward reference consumed by
    :attr:`NoteRequest.assigned_users` when posting a new note.
    """

    id: Optional[int] = Field(None, description="Contact ID — feeds NoteRequest.assigned_users[].id")
    full_name: Optional[str] = Field(None, alias="fullName", description="Display name")

    def cli_format(self) -> str:
        """One-line pretty row used by the CLI and examples (vs. JSON)."""
        id_str = "—" if self.id is None else str(self.id)
        return f"id={id_str:<6} fullName={self.full_name!r}"


# ---------------------------------------------------------------------------
# Response: GET /note
# ---------------------------------------------------------------------------


class GlobalNote(ResponseModel):
    """Note record — element of ``GET /note`` response.

    Shape matches swagger ``Notes``. The server-side field is spelled
    ``modifiyDate`` (sic — typo in the API); the SDK preserves it via alias
    so the Python attribute can use the corrected spelling.
    """

    note_id: Optional[int] = Field(None, alias="noteID", description="Note ID (int)")
    is_important: Optional[bool] = Field(None, alias="isImportant", description="Important flag")
    comments: Optional[str] = Field(None, description="Note content")
    category: Optional[str] = Field(None, description="Category UUID")
    due_date: Optional[datetime] = Field(None, alias="dueDate", description="Due date")
    job_id: Optional[str] = Field(None, alias="jobId", description="Associated job UUID")
    crm_contact_id: Optional[int] = Field(None, alias="crmContactId", description="CRM contact ID (int)")
    contact_id: Optional[str] = Field(None, alias="contactId", description="Contact UUID")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    user_id: Optional[str] = Field(None, alias="userID", description="User UUID")
    importance: Optional[str] = Field(None, description="Importance label")
    author: Optional[str] = Field(None, description="Author display name")
    due_dates: Optional[str] = Field(None, alias="dueDates", description="Due-date label")
    category_name: Optional[str] = Field(None, alias="categoryName", description="Category display name")
    created_date: Optional[datetime] = Field(None, alias="createdDate", description="Created timestamp")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Creator user UUID")
    modified_by: Optional[str] = Field(None, alias="modifiedBy", description="Modifier user UUID")
    modified_date: Optional[datetime] = Field(
        None, alias="modifiyDate", description="Modified timestamp (server spelling: modifiyDate)",
    )
    franchise_id: Optional[str] = Field(None, alias="franchiseID", description="Franchise UUID")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Completion flag")
    is_global: Optional[bool] = Field(None, alias="isGlobal", description="Global flag")
    is_shared: Optional[bool] = Field(None, alias="isShared", description="Shared flag")
    assigned_contact_names: Optional[List[str]] = Field(
        None, alias="assignedContactNames", description="Assigned contact display names",
    )
    assigned_users: Optional[List[SuggestedUser]] = Field(
        None, alias="assignedUsers", description="Assigned users (SuggestedContactEntity[])",
    )
    is_job_level: Optional[bool] = Field(None, alias="isJobLevel", description="Job-scoped note flag")

    def cli_format(self) -> str:
        """One-line pretty row used by the CLI and examples (vs. JSON)."""
        nid = "—" if self.note_id is None else str(self.note_id)
        flags = "".join((
            "!" if self.is_important else "·",
            "✓" if self.is_completed else "·",
            "g" if self.is_global else "·",
            "s" if self.is_shared else "·",
        ))
        modified = self.modified_date.strftime("%Y-%m-%d %H:%M") if self.modified_date else "—"
        cat = (self.category_name or "—")[:18]
        author = (self.author or "—")[:18]
        comment = (self.comments or "").replace("\n", " ")[:60]
        return (
            f"id={nid:<8} "
            f"flags={flags} "
            f"category={cat:<18} "
            f"author={author:<18} "
            f"modified={modified:<16} "
            f"comments={comment!r}"
        )


# ---------------------------------------------------------------------------
# Request: POST /note and PUT /note/{id} (shared schema)
# ---------------------------------------------------------------------------


class NoteRequest(RequestModel):
    """Body for ``POST /note`` **and** ``PUT /note/{id}``.

    Matches swagger ``NoteModel``. The API uses the **same** schema for
    create and update; the legacy ``GlobalNoteCreateRequest`` /
    ``GlobalNoteUpdateRequest`` names are aliases of this class.

    Required fields: ``comments`` (1-8000 chars) and ``category`` (UUID).
    Sourcing ``category``: call ``api.lookup.get_refer_category()`` or
    ``api.lookup.get_refer_category_hierarchy()`` and use a returned
    ``LookupValue.value`` (or ``id``).
    """

    comments: str = Field(..., description="Note content (1-8000 chars)", max_length=8000, min_length=1)
    category: str = Field(..., description="Category UUID (required)")
    due_date: Optional[date] = Field(None, alias="dueDate", description="Due date (yyyy-mm-dd)")
    is_important: Optional[bool] = Field(None, alias="isImportant", description="Mark important")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Mark completed")
    job_id: Optional[str] = Field(None, alias="jobId", description="Job UUID")
    send_notification: Optional[bool] = Field(
        None, alias="sendNotification", description="Send notification to assigned users",
    )
    assigned_users: Optional[List[SuggestedUser]] = Field(
        None, alias="assignedUsers", description="Assigned users (forward ref: SuggestedUser.id)",
    )
    crm_contact_id: Optional[int] = Field(
        None, alias="crmContactId", description="CRM contact ID (int)",
    )
    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    is_global: Optional[bool] = Field(None, alias="isGlobal", description="Global flag")
    is_shared: Optional[bool] = Field(None, alias="isShared", description="Shared flag")


# Backward-compat aliases — single source of truth is NoteRequest.
GlobalNoteCreateRequest = NoteRequest
GlobalNoteUpdateRequest = NoteRequest
