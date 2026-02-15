"""Notes API endpoints (4 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("GET", "/note", response_model="List[GlobalNote]")
_CREATE = Route("POST", "/note", request_model="GlobalNoteCreateRequest", response_model="GlobalNote")
_UPDATE = Route("PUT", "/note/{id}", request_model="GlobalNoteUpdateRequest", response_model="GlobalNote")
_SUGGEST_USERS = Route("GET", "/note/suggestUsers", response_model="List[SuggestedUser]")


class NotesEndpoint(BaseEndpoint):
    """Global note operations (ACPortal API)."""

    def list(self, **params: Any) -> Any:
        """GET /note (params: category, jobId, contactId, companyId)"""
        return self._request(_LIST, params=params or None)

    def create(self, **kwargs: Any) -> Any:
        """POST /note"""
        return self._request(_CREATE, json=kwargs)

    def update(self, note_id: str, **kwargs: Any) -> Any:
        """PUT /note/{id}"""
        return self._request(_UPDATE.bind(id=note_id), json=kwargs)

    def suggest_users(self, **params: Any) -> Any:
        """GET /note/suggestUsers"""
        return self._request(_SUGGEST_USERS, params=params or None)
