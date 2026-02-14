"""Contacts API endpoints (7 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/contacts/{id}", response_model="ContactSimple")
_GET_DETAILS = Route("GET", "/contacts/{contactId}/editdetails", response_model="ContactDetailedInfo")
_UPDATE_DETAILS = Route("PUT", "/contacts/{contactId}/editdetails", request_model="ContactEditRequest")
_CREATE = Route("POST", "/contacts/editdetails", request_model="ContactEditRequest")
_SEARCH = Route("POST", "/contacts/v2/search", request_model="ContactSearchRequest", response_model="List[SearchContactEntityResult]")
_PRIMARY_DETAILS = Route("GET", "/contacts/{contactId}/primarydetails", response_model="ContactPrimaryDetails")
_CURRENT_USER = Route("GET", "/contacts/user", response_model="ContactSimple")


class ContactsEndpoint(BaseEndpoint):
    """Operations on contacts (ACPortal API)."""

    def get(self, contact_id: str) -> Any:
        """GET /contacts/{id}"""
        return self._request(_GET.bind(id=contact_id))

    def get_details(self, contact_id: str) -> Any:
        """GET /contacts/{contactId}/editdetails"""
        return self._request(_GET_DETAILS.bind(contactId=contact_id))

    def update_details(self, contact_id: str, data: dict | Any) -> Any:
        """PUT /contacts/{contactId}/editdetails"""
        return self._request(_UPDATE_DETAILS.bind(contactId=contact_id), json=data)

    def create(self, data: dict | Any) -> Any:
        """POST /contacts/editdetails"""
        return self._request(_CREATE, json=data)

    def search(self, data: dict | Any) -> Any:
        """POST /contacts/v2/search"""
        return self._request(_SEARCH, json=data)

    def get_primary_details(self, contact_id: str) -> Any:
        """GET /contacts/{contactId}/primarydetails"""
        return self._request(_PRIMARY_DETAILS.bind(contactId=contact_id))

    def get_current_user(self) -> Any:
        """GET /contacts/user"""
        return self._request(_CURRENT_USER)
