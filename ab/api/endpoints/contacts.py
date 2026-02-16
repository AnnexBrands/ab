"""Contacts API endpoints (14 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/contacts/{id}", response_model="ContactSimple")
_GET_DETAILS = Route("GET", "/contacts/{contactId}/editdetails", response_model="ContactDetailedInfo")
_UPDATE_DETAILS = Route("PUT", "/contacts/{contactId}/editdetails", request_model="ContactEditRequest")
_CREATE = Route("POST", "/contacts/editdetails", request_model="ContactEditRequest")
_SEARCH = Route(
    "POST", "/contacts/v2/search",
    request_model="ContactSearchRequest", response_model="List[SearchContactEntityResult]",
)
_PRIMARY_DETAILS = Route("GET", "/contacts/{contactId}/primarydetails", response_model="ContactPrimaryDetails")
_CURRENT_USER = Route("GET", "/contacts/user", response_model="ContactSimple")

# Extended contact routes (008)
_POST_HISTORY = Route("POST", "/contacts/{contactId}/history", response_model="ContactHistory")
_GET_HISTORY_AGGREGATED = Route(
    "GET", "/contacts/{contactId}/history/aggregated",
    response_model="ContactHistoryAggregated",
)
_GET_HISTORY_GRAPH_DATA = Route("GET", "/contacts/{contactId}/history/graphdata", response_model="ContactGraphData")
_MERGE_PREVIEW = Route("POST", "/contacts/{mergeToId}/merge/preview", response_model="ContactMergePreview")
_MERGE = Route("PUT", "/contacts/{mergeToId}/merge")


# Extended contacts routes (009)
_POST_CUSTOMERS = Route("POST", "/contacts/customers")
_POST_CONTACTS_SEARCH = Route("POST", "/contacts/search")


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

    # ---- Extended (008) ---------------------------------------------------

    def post_history(self, contact_id: str, **kwargs: Any) -> Any:
        """POST /contacts/{contactId}/history"""
        return self._request(_POST_HISTORY.bind(contactId=contact_id), json=kwargs)

    def get_history_aggregated(self, contact_id: str) -> Any:
        """GET /contacts/{contactId}/history/aggregated"""
        return self._request(_GET_HISTORY_AGGREGATED.bind(contactId=contact_id))

    def get_history_graph_data(self, contact_id: str) -> Any:
        """GET /contacts/{contactId}/history/graphdata"""
        return self._request(_GET_HISTORY_GRAPH_DATA.bind(contactId=contact_id))

    def merge_preview(self, merge_to_id: str, **kwargs: Any) -> Any:
        """POST /contacts/{mergeToId}/merge/preview"""
        return self._request(_MERGE_PREVIEW.bind(mergeToId=merge_to_id), json=kwargs)

    def merge(self, merge_to_id: str, **kwargs: Any) -> Any:
        """PUT /contacts/{mergeToId}/merge"""
        return self._request(_MERGE.bind(mergeToId=merge_to_id), json=kwargs)

    # ---- Extended (009) -----------------------------------------------------

    def get_customers(self, **kwargs: Any) -> Any:
        """POST /contacts/customers"""
        return self._request(_POST_CUSTOMERS, json=kwargs)

    def search_contacts(self, **kwargs: Any) -> Any:
        """POST /contacts/search"""
        return self._request(_POST_CONTACTS_SEARCH, json=kwargs)
