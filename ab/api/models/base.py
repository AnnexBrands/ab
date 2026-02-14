"""Base Pydantic model classes for the ABConnect SDK.

Provides the model hierarchy:

- ``ABConnectBaseModel`` — shared config (camelCase aliases, populate_by_name).
- ``RequestModel`` — ``extra="forbid"`` for strict outbound validation.
- ``ResponseModel`` — ``extra="allow"`` with ``logger.warning`` for unknown
  fields, giving production resilience with immediate drift visibility.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Type, TypeVar, Union

from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)

T = TypeVar("T", bound="ABConnectBaseModel")


def _to_camel(name: str) -> str:
    """Convert ``snake_case`` to ``camelCase``."""
    parts = name.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:])


class ABConnectBaseModel(BaseModel):
    """Root base class for all ABConnect models.

    All fields use **snake_case** in Python with **camelCase** aliases for
    JSON serialization.  ``populate_by_name=True`` allows construction using
    either convention.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=_to_camel,
        str_strip_whitespace=True,
        use_enum_values=True,
    )

    @classmethod
    def check(
        cls: Type[T],
        data: Union[Dict[str, Any], List[Dict[str, Any]], T, List[T]],
        exclude_unset: bool = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Validate *data* and return a JSON-ready dict (or list of dicts).

        Keys are camelCase (``by_alias=True``) and special types
        (datetime, UUID, …) are serialized to JSON-compatible formats.
        """
        if isinstance(data, list):
            validated = [cls.model_validate(item) for item in data]
            return [
                item.model_dump(by_alias=True, exclude_none=True, exclude_unset=exclude_unset, mode="json")
                for item in validated
            ]
        validated = cls.model_validate(data)
        return validated.model_dump(by_alias=True, exclude_none=True, exclude_unset=exclude_unset, mode="json")

    def __repr__(self) -> str:
        fields = self.model_dump(exclude_none=True, by_alias=True)
        if not fields:
            return f"{self.__class__.__name__}()"
        lines = [f"{self.__class__.__name__}("]
        for key, value in fields.items():
            lines.append(f"    {key}={value!r},")
        lines.append(")")
        return "\n".join(lines)


class RequestModel(ABConnectBaseModel):
    """Base for **outbound** request bodies.

    ``extra="forbid"`` catches typos and invalid fields at construction time.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        alias_generator=_to_camel,
        str_strip_whitespace=True,
        use_enum_values=True,
    )


class ResponseModel(ABConnectBaseModel):
    """Base for **inbound** API response bodies.

    ``extra="allow"`` keeps deserialization resilient when the API adds new
    fields.  Unknown fields are stored in ``model_extra`` and a
    ``logger.warning`` is emitted for each one so drift is immediately
    visible.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        alias_generator=_to_camel,
        str_strip_whitespace=True,
        use_enum_values=True,
    )

    def model_post_init(self, __context: Any) -> None:
        if self.model_extra:
            cls_name = self.__class__.__name__
            for field_name in self.model_extra:
                logger.warning(
                    "%s received unexpected field '%s' — consider adding it to the model",
                    cls_name,
                    field_name,
                )
