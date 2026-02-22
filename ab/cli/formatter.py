"""Result formatting for CLI output."""

from __future__ import annotations

import json
from typing import Any


def format_result(result: Any) -> str:
    """Format an API response for stdout output."""
    from pydantic import BaseModel

    if result is None:
        return "null"

    if isinstance(result, bytes):
        return f"<binary response, {len(result)} bytes>"

    if isinstance(result, BaseModel):
        return json.dumps(result.model_dump(by_alias=True, mode="json"), indent=2)

    if isinstance(result, list):
        items = []
        for item in result:
            if isinstance(item, BaseModel):
                items.append(item.model_dump(by_alias=True, mode="json"))
            else:
                items.append(item)
        return json.dumps(items, indent=2)

    if isinstance(result, dict):
        return json.dumps(result, indent=2)

    # Primitive types (str, int, bool, float)
    return str(result)
