"""Job item helpers — lenient create/replace/update/delete for parcel & freight.

Exposed as ``api.jobs.items``. A thin, ergonomic layer over the routed
parcel-item and freight-item endpoints that:

* accepts loose keyword input and silently drops keys the request model does
  not declare, so callers never fight ``extra="forbid"`` validation — i.e. the
  pydantic model never "squawks";
* implements freight's *replace-all* semantics with get-merge-write, so
  updating or deleting one freight item preserves the others (the freight
  endpoint takes a full ``SaveAllFreightItemsRequest`` and has no per-item
  routes); and
* round-trips GET responses (now drift-free, see :class:`JobFreightItem`) back
  into requests losslessly.

Like :class:`~ab.api.helpers.timeline.TimelineHelpers` and
:class:`~ab.api.helpers.agent.AgentHelpers`, this is a plain helper (not a
routed :class:`~ab.api.base.BaseEndpoint` subgroup): it composes existing
endpoints and introduces no new routes.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Iterable

from ab.api.models.jobs import (
    FreightShipment,
    ItemUpdateRequest,
    ParcelItemCreateRequest,
)

if TYPE_CHECKING:
    from ab.api.endpoints.jobs import JobsEndpoint
    from ab.api.models.jobs import JobFreightItem, ParcelItem
    from ab.api.models.shared import ServiceBaseResponse

logger = logging.getLogger(__name__)

#: Friendly shorthand → ``FreightShipment`` python field names, so callers can
#: write ``replace_freight(job, fid, weight=120, length=10)`` without knowing
#: the item/total field split.
_FREIGHT_SHORTHAND = {
    "weight": "item_weight",
    "length": "item_length",
    "width": "item_width",
    "height": "item_height",
    "value": "item_value",
    "description": "freight_description",
    "freight_class": "freight_item_class",
    "nmfc": "nmfc_item",
}


def _known_keys(model_cls: type) -> set[str]:
    """Every field name and alias a model accepts."""
    keys: set[str] = set()
    for name, field in model_cls.model_fields.items():
        keys.add(name)
        if field.alias:
            keys.add(field.alias)
    return keys


def _filtered(model_cls: type, data: dict) -> dict:
    """Drop keys *model_cls* does not declare so ``extra="forbid"`` never trips."""
    allowed = _known_keys(model_cls)
    kept = {k: v for k, v in data.items() if k in allowed}
    dropped = sorted(set(data) - set(kept))
    if dropped:
        logger.debug("%s: dropped unrecognized keys %s", model_cls.__name__, dropped)
    return kept


def _normalize_freight_fields(fields: dict) -> dict:
    """Apply freight shorthand, then keep only ``FreightShipment`` keys."""
    translated: dict[str, Any] = {}
    allowed = _known_keys(FreightShipment)
    for key, value in fields.items():
        if key in allowed:
            translated[key] = value
        elif key in _FREIGHT_SHORTHAND:
            translated[_FREIGHT_SHORTHAND[key]] = value
        else:
            logger.debug("FreightShipment: dropped unrecognized key %r", key)
    return translated


class JobItemsHelpers:
    """Lenient parcel/freight item operations — ``api.jobs.items``."""

    def __init__(self, jobs: JobsEndpoint) -> None:
        self._jobs = jobs

    # ---- Parcel items -------------------------------------------------------

    def list_parcel(self, job_display_id: int) -> list[ParcelItem]:
        """Return the job's parcel items (``GET /job/{id}/parcelitems``)."""
        return self._jobs.parcel_items.list(job_display_id)

    def upsert_parcel(self, job_display_id: int, *, description: str, **fields: Any) -> ParcelItem:
        """Create a parcel item, dropping any kwargs the create body rejects.

        ``description`` is required by the API; ``length``, ``width``,
        ``height``, ``weight`` and ``quantity`` are accepted. Unknown kwargs are
        ignored rather than raising.
        """
        data = _filtered(ParcelItemCreateRequest, {"description": description, **fields})
        return self._jobs.parcel_items.create(job_display_id, data=data)

    def update_parcel(self, job_display_id: int, item_id: str, **fields: Any) -> ServiceBaseResponse:
        """Update a parcel item in place via ``PUT /job/{id}/item/{itemId}``.

        Only ``description``, ``quantity`` and ``weight`` are sent; other kwargs
        are dropped so the strict update body never rejects the call.
        """
        data = _filtered(ItemUpdateRequest, fields)
        return self._jobs.update_item(job_display_id, str(item_id), data=data)

    def delete_parcel(self, job_display_id: int, parcel_item_id: str) -> ServiceBaseResponse:
        """Delete a parcel item (``DELETE /job/{id}/parcelitems/{parcelItemId}``)."""
        return self._jobs.parcel_items.delete(job_display_id, str(parcel_item_id))

    def replace_parcel(
        self, job_display_id: int, parcel_item_id: str, *, description: str, **fields: Any
    ) -> ParcelItem:
        """Replace a parcel item: delete the existing one, then create a fresh one.

        The parcel endpoint exposes no PUT, so "replace" is delete + create.
        Returns the newly created :class:`ParcelItem`.
        """
        self._jobs.parcel_items.delete(job_display_id, str(parcel_item_id))
        return self.upsert_parcel(job_display_id, description=description, **fields)

    # ---- Freight items (get-merge-write; replace-all) -----------------------

    def list_freight(self, job_display_id: int) -> list[JobFreightItem]:
        """Return the job's current freight items (from ``GET /job/{id}``)."""
        job = self._jobs.get(job_display_id)
        return list(getattr(job, "freight_items", None) or [])

    def _current_freight_dicts(self, job_display_id: int) -> list[dict]:
        """Current freight items as ``FreightShipment``-shaped camelCase dicts."""
        return [
            _filtered(FreightShipment, item.model_dump(by_alias=True, exclude_none=True))
            for item in self.list_freight(job_display_id)
        ]

    @staticmethod
    def _matches(item: dict, *, freight_item_id: str | None, item_id: str | None) -> bool:
        if freight_item_id is not None and item.get("freightItemId") == freight_item_id:
            return True
        return item_id is not None and item.get("itemID") == item_id

    def set_freight(
        self, job_display_id: int, items: Iterable[Any], *, force_update: bool = True
    ) -> list[JobFreightItem]:
        """Replace ALL freight items on the job with *items* (full save).

        Each item may be a :class:`FreightShipment`/:class:`JobFreightItem`
        model or a plain dict; unrecognized keys are dropped. ``force_update``
        bypasses the job's optimistic-concurrency check. Returns the refreshed
        freight items so the caller can confirm the resulting state.
        """
        payload = []
        for item in items:
            raw = item.model_dump(by_alias=True, exclude_none=True) if hasattr(item, "model_dump") else dict(item)
            payload.append(_filtered(FreightShipment, raw))
        self._jobs.add_freight_items(
            job_display_id,
            data={"freightItems": payload, "forceUpdate": force_update},
        )
        return self.list_freight(job_display_id)

    def upsert_freight(
        self,
        job_display_id: int,
        *,
        freight_item_id: str | None = None,
        item_id: str | None = None,
        **fields: Any,
    ) -> list[JobFreightItem]:
        """Add or update one freight item while preserving the others.

        Identifies the target by ``freight_item_id`` or ``item_id``; merges the
        given fields onto it (or appends a new item when none matches), then
        saves the full set. Accepts friendly shorthand (``weight``, ``length``,
        …) as well as exact field names/aliases.
        """
        current = self._current_freight_dicts(job_display_id)
        new_fields = _normalize_freight_to_camel(fields)
        matched = False
        for item in current:
            if self._matches(item, freight_item_id=freight_item_id, item_id=item_id):
                item.update(new_fields)
                matched = True
        if not matched:
            fresh: dict[str, Any] = {}
            if freight_item_id is not None:
                fresh["freightItemId"] = freight_item_id
            if item_id is not None:
                fresh["itemID"] = item_id
            fresh.update(new_fields)
            current.append(fresh)
        return self.set_freight(job_display_id, current)

    def replace_freight(self, job_display_id: int, freight_item_id: str, **fields: Any) -> list[JobFreightItem]:
        """Overwrite the matching freight item's fields, preserving the others."""
        return self.upsert_freight(job_display_id, freight_item_id=freight_item_id, **fields)

    def delete_freight(self, job_display_id: int, freight_item_id: str) -> list[JobFreightItem]:
        """Remove one freight item by saving the remaining set (no DELETE route)."""
        current = self._current_freight_dicts(job_display_id)
        remaining = [
            item for item in current if not self._matches(item, freight_item_id=freight_item_id, item_id=None)
        ]
        return self.set_freight(job_display_id, remaining)


def _normalize_freight_to_camel(fields: dict) -> dict:
    """Normalize loose kwargs to camelCase ``FreightShipment`` keys via the model."""
    snake = _normalize_freight_fields(fields)
    # Round-trip through the request model to get camelCase aliases + type
    # coercion, dropping nothing (already filtered) and never raising on extras.
    model = FreightShipment.model_validate(snake)
    return model.model_dump(by_alias=True, exclude_unset=True)
