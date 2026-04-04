"""Lot models for the Catalog API.

Field shapes ported against ``ab/api/schemas/catalog.json`` (swagger,
Tier 3) with ``ABConnectTools/ABConnect/api/models/catalog.py`` as
secondary reference (Tier 4). The prior placeholder implementation
had invented field names that did not match either source — see
``specs/036-lotsdb-migration-prep/gap-recommendations.md`` for the
full drift history.

Casing note: the Catalog API uses mixed PascalCase / camelCase for
``LotDataDto`` field aliases (``Qty``, ``L``, ``W``, ``H``, ``Wgt``,
``Cpack``, ``ItemID``, ``Notes`` are PascalCase; ``value``,
``description``, ``forceCrate``, ``doNotTip``, ``commodityId``,
``notedConditions`` are camelCase). Aliases below match swagger
exactly. ABConnectTools used uniform PascalCase on writes (``CPack``);
when in doubt swagger wins per the constitution's Sources of Truth
hierarchy.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import AliasChoices, ConfigDict, Field, field_validator

from ab.api.models.base import RequestModel, ResponseModel


class LotDataDto(ResponseModel):
    """Nested data payload shared by lot reads and writes.

    Used in both response contexts (``LotDto.initial_data``) and request
    contexts (``AddLotRequest.initial_data``, ``BulkInsertLotRequest.initial_data``).
    ``extra="ignore"`` is used instead of the default ``allow`` because
    the API occasionally echoes keys from related entities back into
    nested lot data.
    """

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        str_strip_whitespace=True,
        use_enum_values=True,
    )

    qty: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("Qty", "qty"),
        serialization_alias="Qty",
        description="Quantity",
    )
    length: Optional[float] = Field(
        None,
        validation_alias=AliasChoices("L", "l"),
        serialization_alias="L",
        description="Length",
    )
    width: Optional[float] = Field(
        None,
        validation_alias=AliasChoices("W", "w"),
        serialization_alias="W",
        description="Width",
    )
    height: Optional[float] = Field(
        None,
        validation_alias=AliasChoices("H", "h"),
        serialization_alias="H",
        description="Height",
    )
    weight: Optional[float] = Field(
        None,
        validation_alias=AliasChoices("Wgt", "wgt"),
        serialization_alias="Wgt",
        description="Weight",
    )
    value: Optional[float] = Field(
        None,
        validation_alias=AliasChoices("value", "Value"),
        serialization_alias="value",
        description="Declared value",
    )
    cpack: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("Cpack", "CPack", "cpack"),
        serialization_alias="Cpack",
        description="Container pack ID",
    )
    description: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("description", "Description"),
        serialization_alias="description",
        description="Item description",
    )
    force_crate: Optional[bool] = Field(
        None,
        validation_alias=AliasChoices("forceCrate", "ForceCrate"),
        serialization_alias="forceCrate",
        description="Force crating flag",
    )
    item_id: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ItemID", "itemID", "itemId"),
        serialization_alias="ItemID",
        description="Item ID (string per swagger; ABConnectTools treated as int)",
    )
    notes: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("Notes", "notes"),
        serialization_alias="Notes",
        description="Free-text notes",
    )
    noted_conditions: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("notedConditions", "NotedConditions"),
        serialization_alias="notedConditions",
        description="Recorded conditions",
    )
    do_not_tip: Optional[bool] = Field(
        None,
        validation_alias=AliasChoices("doNotTip", "DoNotTip"),
        serialization_alias="doNotTip",
        description="Do-not-tip flag",
    )
    commodity_id: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("commodityId", "CommodityId"),
        serialization_alias="commodityId",
        description="Commodity / HS code ID (string per swagger)",
    )

    @field_validator("qty", mode="before")
    @classmethod
    def _empty_string_to_none(cls, v):  # noqa: D401
        """Coerce empty strings to None for optional int fields."""
        return None if v == "" else v


class ImageLinkDto(ResponseModel):
    """Image link reference."""

    id: int = Field(..., description="Image ID")
    link: Optional[str] = Field(None, description="Image URL")


class LotCatalogDto(ResponseModel):
    """Lot-to-catalog association. Also used as a body fragment in
    :class:`AddLotRequest` and :class:`UpdateLotRequest`."""

    catalog_id: int = Field(..., alias="catalogId", description="Parent catalog ID")
    lot_number: Optional[str] = Field(None, alias="lotNumber", description="Lot number within catalog")


class LotCatalogInformationDto(ResponseModel):
    """Basic lot information embedded in a catalog response."""

    id: int = Field(..., description="Lot ID")
    lot_number: Optional[str] = Field(None, alias="lotNumber", description="Lot number")


class LotDto(ResponseModel):
    """Full lot — returned by ``POST /Lot`` and ``GET /Lot/{id}``."""

    id: int = Field(..., description="Lot ID")
    customer_item_id: Optional[str] = Field(None, alias="customerItemId", description="Customer item ID")
    initial_data: Optional[LotDataDto] = Field(None, alias="initialData", description="Initial lot data")
    overriden_data: Optional[List[LotDataDto]] = Field(
        None, alias="overridenData", description="Override entries",
    )
    catalogs: Optional[List[LotCatalogDto]] = Field(
        None, description="Catalog associations (each entry is a LotCatalogDto)",
    )
    image_links: Optional[List[ImageLinkDto]] = Field(
        None, alias="imageLinks", description="Attached image links",
    )


class LotOverrideDto(LotDataDto):
    """Lot override data keyed by customer item ID.

    Inherits every field from :class:`LotDataDto` and adds
    ``customerItemId``. Used by ``POST /Lot/get-overrides``.
    """

    customer_item_id: Optional[str] = Field(
        None, alias="customerItemId", description="Customer item ID the override applies to",
    )


class AddLotRequest(RequestModel):
    """Body for ``POST /Lot``.

    All fields are optional per swagger — the server will reject an
    empty body with a 400 on its own side; the SDK does not duplicate
    that validation because swagger does not declare required fields.
    Callers typically supply at minimum ``customer_item_id``, ``catalogs``,
    and ``initial_data``.
    """

    customer_item_id: Optional[str] = Field(None, alias="customerItemId", description="Customer item ID")
    image_links: Optional[List[str]] = Field(
        None, alias="imageLinks", description="Image URLs attached to the lot",
    )
    overriden_data: Optional[List[LotDataDto]] = Field(
        None, alias="overridenData", description="Per-catalog override data entries",
    )
    catalogs: Optional[List[LotCatalogDto]] = Field(
        None, description="Catalogs this lot belongs to",
    )
    initial_data: Optional[LotDataDto] = Field(None, alias="initialData", description="Initial lot measurements")


class UpdateLotRequest(RequestModel):
    """Body for ``PUT /Lot/{id}``. Note: no ``initialData`` — updates
    cannot change the initial measurements."""

    customer_item_id: Optional[str] = Field(None, alias="customerItemId", description="Customer item ID")
    image_links: Optional[List[str]] = Field(
        None, alias="imageLinks", description="Image URLs attached to the lot",
    )
    overriden_data: Optional[List[LotDataDto]] = Field(
        None, alias="overridenData", description="Per-catalog override data entries",
    )
    catalogs: Optional[List[LotCatalogDto]] = Field(
        None, description="Catalogs this lot belongs to",
    )


class LotListParams(RequestModel):
    """Query parameters for ``GET /Lot``."""

    id: Optional[int] = Field(None, alias="Id", description="Filter by lot ID")
    customer_item_id: Optional[str] = Field(None, alias="CustomerItemId", description="Filter by customer item ID")
    lot_number: Optional[str] = Field(None, alias="LotNumber", description="Filter by lot number")
    page_size: Optional[int] = Field(None, alias="PageSize", description="Number of items per page")
    page_number: Optional[int] = Field(None, alias="PageNumber", description="Page number")
