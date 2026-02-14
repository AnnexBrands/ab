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
        street: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        country: Optional[str] = None,
    ) -> Any:
        """GET /address/isvalid"""
        params: dict[str, str] = {}
        if street:
            params["street"] = street
        if city:
            params["city"] = city
        if state:
            params["state"] = state
        if zip_code:
            params["zipCode"] = zip_code
        if country:
            params["country"] = country
        return self._request(_IS_VALID, params=params)

    def get_property_type(self, *, street: str, zip_code: str) -> Any:
        """GET /address/propertytype"""
        return self._request(_PROPERTY_TYPE, params={"street": street, "zipCode": zip_code})
