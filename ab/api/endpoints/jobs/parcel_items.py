"""Job-scoped parcel-item operations — swagger tag ``JobParcelItems`` (4 routes).

Exposed as ``api.jobs.parcel_items``. Old names on
:class:`~ab.api.endpoints.jobs.JobsEndpoint` remain as deprecation shims.

Method renames (``_parcel_items?`` suffix dropped):

* :meth:`list`                  (was ``get_parcel_items``)
* :meth:`create`                (was ``create_parcel_item``)
* :meth:`delete`                (was ``delete_parcel_item``)
* :meth:`list_with_materials`   (was ``get_parcel_items_with_materials``)

Note: ``get_packaging_containers`` (``/packagingcontainers``),
``update_item`` (``/item/{id}``), and ``add_item_notes``
(``/item/notes``) are tagged ``Job`` in swagger, not
``JobParcelItems``, so they remain on :class:`JobsEndpoint`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.jobs import (
        ParcelItem,
        ParcelItemCreateRequest,
        ParcelItemWithMaterials,
    )
    from ab.api.models.shared import ServiceBaseResponse

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("GET", "/job/{jobDisplayId}/parcelitems", response_model="List[ParcelItem]")
_CREATE = Route(
    "POST",
    "/job/{jobDisplayId}/parcelitems",
    request_model="ParcelItemCreateRequest",
    response_model="ParcelItem",
)
_DELETE = Route(
    "DELETE",
    "/job/{jobDisplayId}/parcelitems/{parcelItemId}",
    response_model="ServiceBaseResponse",
)
_LIST_WITH_MATERIALS = Route(
    "GET",
    "/job/{jobDisplayId}/parcel-items-with-materials",
    response_model="List[ParcelItemWithMaterials]",
)


class JobParcelItemsEndpoint(BaseEndpoint):
    """Job-scoped parcel-item operations (ACPortal API)."""

    def list(self, job_display_id: int) -> list[ParcelItem]:
        """``GET /job/{jobDisplayId}/parcelitems``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/parcel_items.list.html
        Response model: List[ParcelItem]
        """
        return self._request(_LIST.bind(jobDisplayId=job_display_id))

    def create(
        self,
        job_display_id: int,
        *,
        data: ParcelItemCreateRequest | dict,
    ) -> ParcelItem:
        """``POST /job/{jobDisplayId}/parcelitems``

        Request model: :class:`ParcelItemCreateRequest`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/parcel_items.create.html
        Request model: ParcelItemCreateRequest
        Response model: ParcelItem
        """
        return self._request(_CREATE.bind(jobDisplayId=job_display_id), json=data)

    def delete(self, job_display_id: int, parcel_item_id: str) -> ServiceBaseResponse:
        """``DELETE /job/{jobDisplayId}/parcelitems/{parcelItemId}``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/parcel_items.delete.html
        Response model: ServiceBaseResponse
        """
        return self._request(
            _DELETE.bind(jobDisplayId=job_display_id, parcelItemId=parcel_item_id),
        )

    def list_with_materials(self, job_display_id: int) -> list[ParcelItemWithMaterials]:
        """``GET /job/{jobDisplayId}/parcel-items-with-materials``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/parcel_items.list_with_materials.html
        Response model: List[ParcelItemWithMaterials]
        """
        return self._request(_LIST_WITH_MATERIALS.bind(jobDisplayId=job_display_id))
