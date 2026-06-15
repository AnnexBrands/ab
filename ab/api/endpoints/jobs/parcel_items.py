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
# POST /parcelitems is replace-all (SaveAllParcelItemsRequest): the body's
# parcelItems array becomes the ENTIRE set. `save` exposes that directly; `create`
# reads the current set and merges one item so existing items are not wiped.
_SAVE = Route(
    "POST",
    "/job/{jobDisplayId}/parcelitems",
    request_model="ParcelItemsRequest",
    response_model="ParcelItemsResponse",
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
        """Add ONE parcel item, preserving the existing set (ACID get-merge-write).

        ``POST /job/{jobDisplayId}/parcelitems`` is replace-all
        (``SaveAllParcelItemsRequest``): the body's ``parcelItems`` array becomes
        the ENTIRE set. To avoid wiping the other items, this reads the current
        parcel items, appends *data* (an ergonomic single-item
        :class:`ParcelItemCreateRequest`), and saves the full set. Returns the
        newly added :class:`ParcelItem`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/parcel_items.create.html
        Request model: ParcelItemsRequest
        Response model: ParcelItemsResponse
        """
        from ab.api.models.jobs import ParcelItemCreateRequest as _CreateReq
        from ab.api.models.jobs import ParcelItemSave as _Save

        one = _CreateReq.check(data)
        new_item = {
            "description": one.get("description"),
            "quantity": one.get("quantity"),
            "jobItemPkdLength": one.get("length"),
            "jobItemPkdWidth": one.get("width"),
            "jobItemPkdHeight": one.get("height"),
            "jobItemPkdWeight": one.get("weight"),
        }
        new_item = {k: v for k, v in new_item.items() if v is not None}

        allowed = {f.alias or n for n, f in _Save.model_fields.items()}
        existing = self.list(job_display_id)
        before_ids = {p.id for p in existing if getattr(p, "id", None) is not None}
        payload = [
            {k: v for k, v in p.model_dump(by_alias=True, exclude_none=True).items() if k in allowed}
            for p in existing
        ]
        payload.append(new_item)

        resp = self._request(
            _SAVE.bind(jobDisplayId=job_display_id),
            json={"parcelItems": payload, "forceUpdate": True},
        )
        after = list(getattr(resp, "parcel_items", None) or [])
        for p in after:
            if getattr(p, "id", None) is not None and p.id not in before_ids:
                return p
        return after[-1] if after else self._resolve_model("ParcelItem").model_validate(new_item)

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
