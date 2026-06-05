"""Job-scoped freight-provider operations — swagger tag ``JobFreightProviders`` (3 routes).

Exposed as ``api.jobs.freight_providers``. Old names on
:class:`~ab.api.endpoints.jobs.JobsEndpoint` remain as deprecation shims.

Method renames (``_freight_provider(s)`` suffix dropped):

* :meth:`list`           (was ``list_freight_providers``)
* :meth:`save`           (was ``save_freight_providers``)
* :meth:`rate_quote`     (was ``get_freight_provider_rate_quote``)

Note: ``add_freight_items`` is tagged ``Job`` in swagger, not
``JobFreightProviders``, so it remains on :class:`JobsEndpoint`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.jobs import (
        PricedFreightProvider,
        RateQuoteRequest,
        ShipmentPlanProvider,
    )

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route(
    "GET",
    "/job/{jobDisplayId}/freightproviders",
    params_model="FreightProvidersParams",
    response_model="List[PricedFreightProvider]",
)
_SAVE = Route(
    "POST",
    "/job/{jobDisplayId}/freightproviders",
    request_model="ShipmentPlanProvider",
)
_RATE_QUOTE = Route(
    "POST",
    "/job/{jobDisplayId}/freightproviders/{optionIndex}/ratequote",
    request_model="RateQuoteRequest",
)


class JobFreightProvidersEndpoint(BaseEndpoint):
    """Job-scoped freight-provider operations (ACPortal API)."""

    def list(
        self,
        job_display_id: int,
        *,
        provider_indexes: list[int] | None = None,
        shipment_types: list[str] | None = None,
        only_active: bool | None = None,
    ) -> list[PricedFreightProvider]:
        """``GET /job/{jobDisplayId}/freightproviders``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/freight_providers.list.html
        Query params: FreightProvidersParams
        Response model: List[PricedFreightProvider]
        """
        return self._request(
            _LIST.bind(jobDisplayId=job_display_id),
            params=dict(
                provider_indexes=provider_indexes,
                shipment_types=shipment_types,
                only_active=only_active,
            ),
        )

    def save(self, job_display_id: int, *, data: ShipmentPlanProvider | dict) -> None:
        """``POST /job/{jobDisplayId}/freightproviders``

        Request model: :class:`ShipmentPlanProvider`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/freight_providers.save.html
        Request model: ShipmentPlanProvider
        """
        return self._request(_SAVE.bind(jobDisplayId=job_display_id), json=data)

    def rate_quote(
        self,
        job_display_id: int,
        option_index: int,
        *,
        data: RateQuoteRequest | dict,
    ) -> None:
        """``POST /job/{jobDisplayId}/freightproviders/{optionIndex}/ratequote``

        Request model: :class:`RateQuoteRequest`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/freight_providers.rate_quote.html
        Request model: RateQuoteRequest
        """
        return self._request(
            _RATE_QUOTE.bind(jobDisplayId=job_display_id, optionIndex=option_index),
            json=data,
        )
