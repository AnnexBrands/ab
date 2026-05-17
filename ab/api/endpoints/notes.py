"""Notes API endpoints (4 routes).

Swagger reveals one schema (``NoteModel``) for **both** ``POST /note`` and
``PUT /note/{id}``. The SDK reflects that with a single :class:`NoteRequest`.
The endpoint class still exposes :meth:`create` and :meth:`update` as
separate methods because the path and HTTP verb differ.

Discovery chain for ``create``: ``api.lookup.get_refer_categories`` /
``get_refer_category_hierarchy`` returns category UUIDs that feed
:attr:`NoteRequest.category`; ``suggest_users`` returns ``SuggestedUser``
records whose ``id`` feeds :attr:`NoteRequest.assigned_users`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.notes import GlobalNote, NoteRequest, SuggestedUser

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("GET", "/note", params_model="NotesListParams", response_model="List[GlobalNote]")
_CREATE = Route("POST", "/note", request_model="NoteRequest", response_model="GlobalNote")
_UPDATE = Route("PUT", "/note/{id}", request_model="NoteRequest", response_model="GlobalNote")
_SUGGEST_USERS = Route(
    "GET", "/note/suggestUsers", params_model="NotesSuggestUsersParams", response_model="List[SuggestedUser]"
)


class NotesEndpoint(BaseEndpoint):
    """Global note operations (ACPortal API).

    Forward references:

    * ``api.lookup.get_refer_categories`` -> :attr:`NoteRequest.category`
    * :meth:`suggest_users` -> :attr:`NoteRequest.assigned_users` (by ``id``)
    """

    def list(
        self,
        *,
        category: list[str] | None = None,
        job_id: str | None = None,
        contact_id: int | None = None,
        company_id: str | None = None,
    ) -> list[GlobalNote]:
        """List notes (``GET /note``).

        Swagger marks every filter optional, but the **live API requires at
        least one** of ``category``, ``job_id``, ``contact_id``, or
        ``company_id`` -- omitting them all returns HTTP 400. The SDK
        relays whatever the caller passes; it does not impose this rule.

        Args:
            category: One or more category UUIDs (repeated query param).
            job_id: Filter to notes attached to this job UUID.
            contact_id: Filter to notes attached to this contact ID.
            company_id: Filter to notes attached to this company UUID.
        """
        return self._request(
            _LIST,
            params=dict(category=category, job_id=job_id, contact_id=contact_id, company_id=company_id),
        )

    def create(self, *, data: NoteRequest | dict) -> GlobalNote:
        """Create a note (``POST /note``).

        Args:
            data: Note payload. Accepts a :class:`NoteRequest` instance or
                a dict. ``comments`` and ``category`` are **required** by
                swagger; the request model enforces this.

        Request model: :class:`NoteRequest` (same schema as ``update``).
        """
        return self._request(_CREATE, json=data)

    def update(self, note_id: str, *, data: NoteRequest | dict) -> GlobalNote:
        """Update a note (``PUT /note/{id}``).

        The API uses the same :class:`NoteRequest` schema as ``create``, so
        ``comments`` and ``category`` are required on update too -- partial
        updates are not supported by this endpoint.

        Args:
            note_id: Note identifier (path param).
            data: Note payload. Accepts a :class:`NoteRequest` instance or
                a dict.

        Request model: :class:`NoteRequest` (same schema as ``create``).
        """
        return self._request(_UPDATE.bind(id=note_id), json=data)

    def suggest_users(
        self,
        search_key: str,
        *,
        job_franchisee_id: str | None = None,
        company_id: str | None = None,
    ) -> list[SuggestedUser]:
        """Suggest users for mentions (``GET /note/suggestUsers``).

        ``search_key`` is **required** by swagger; it is positional here so
        it cannot be silently omitted.

        Returns rows whose ``id`` feeds :attr:`NoteRequest.assigned_users`.
        """
        return self._request(
            _SUGGEST_USERS,
            params=dict(search_key=search_key, job_franchisee_id=job_franchisee_id, company_id=company_id),
        )
