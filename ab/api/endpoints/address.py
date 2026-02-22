"""Address API endpoints (2 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ab.api.models.address import AddressIsValidResult

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_IS_VALID = Route(
    "GET", "/address/isvalid", params_model="AddressValidateParams", response_model="AddressIsValidResult"
)
_PROPERTY_TYPE = Route(
    "GET", "/address/propertytype", params_model="AddressPropertyTypeParams", response_model="int"
)


class AddressEndpoint(BaseEndpoint):
    """Address validation (ACPortal API)."""

    def validate(
        self,
        *,
        line1: str,
        city: str,
        state: str,
        zip: str
    ) -> AddressIsValidResult:
        """GET /address/isvalid"""
        return self._request(
            _IS_VALID, params=dict(line1=line1, city=city, state=state, zip=zip)
        )

    def get_property_type(
        self,
        *,
        address1: str,
        address2: Optional[str] = None,
        city: str,
        state: str,
        zip_code: str,
    ) -> Optional[int]:
        """GET /address/propertytype"""
        return self._request(
            _PROPERTY_TYPE,
            params=dict(
                address1=address1, address2=address2, city=city, state=state, zip_code=zip_code
            ),
        )
