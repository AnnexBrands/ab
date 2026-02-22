"""Notes API endpoints (4 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.notes import GlobalNote, SuggestedUser

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("GET", "/note", params_model="NotesListParams", response_model="List[GlobalNote]")
_CREATE = Route("POST", "/note", request_model="GlobalNoteCreateRequest", response_model="GlobalNote")
_UPDATE = Route("PUT", "/note/{id}", request_model="GlobalNoteUpdateRequest", response_model="GlobalNote")
_SUGGEST_USERS = Route(
    "GET", "/note/suggestUsers", params_model="NotesSuggestUsersParams", response_model="List[SuggestedUser]"
)


class NotesEndpoint(BaseEndpoint):
    """Global note operations (ACPortal API)."""

    def list(
        self,
        *,
        category: list[str] | None = None,
        job_id: str | None = None,
        contact_id: int | None = None,
        company_id: str | None = None,
    ) -> list[GlobalNote]:
        """GET /note (params: category, jobId, contactId, companyId)"""
        return self._request(
            _LIST,
            params=dict(category=category, job_id=job_id, contact_id=contact_id, company_id=company_id),
        )

    def create(self, **kwargs: Any) -> GlobalNote:
        """POST /note"""
        return self._request(_CREATE, json=kwargs)

    def update(self, note_id: str, **kwargs: Any) -> GlobalNote:
        """PUT /note/{id}"""
        return self._request(_UPDATE.bind(id=note_id), json=kwargs)

    def suggest_users(
        self,
        *,
        search_key: str,
        job_franchisee_id: str | None = None,
        company_id: str | None = None,
    ) -> list[SuggestedUser]:
        """GET /note/suggestUsers"""
        return self._request(
            _SUGGEST_USERS,
            params=dict(search_key=search_key, job_franchisee_id=job_franchisee_id, company_id=company_id),
        )
