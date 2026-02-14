"""Address API endpoints (2 routes)."""

from __future__ import annotations

from typing import Any, Optional

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_IS_VALID = Route("GET", "/address/isvalid", response_model="AddressIsValidResult")
_PROPERTY_TYPE = Route("GET", "/address/propertytype", response_model="PropertyType")


class AddressEndpoint(BaseEndpoint):
    """Address validation (ACPortal API)."""

    def validate(
        self,
        *,
        line1: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip: Optional[str] = None,
    ) -> Any:
        """GET /address/isvalid"""
        params: dict[str, str] = {}
        if line1:
            params["Line1"] = line1
        if city:
            params["City"] = city
        if state:
            params["State"] = state
        if zip:
            params["Zip"] = zip
        return self._request(_IS_VALID, params=params)

    def get_property_type(
        self,
        *,
        address1: Optional[str] = None,
        address2: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
    ) -> Any:
        """GET /address/propertytype"""
        params: dict[str, str] = {}
        if address1:
            params["Address1"] = address1
        if address2:
            params["Address2"] = address2
        if city:
            params["City"] = city
        if state:
            params["State"] = state
        if zip_code:
            params["ZipCode"] = zip_code
        return self._request(_PROPERTY_TYPE, params=params)
