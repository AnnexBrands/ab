"""Result formatting for CLI output.

Two output modes:

* **Pretty** (default): if the result model implements ``cli_format() -> str``
  that's used. Lists of such models are joined with newlines.
* **JSON** (``as_json=True``): always emit ``json.dumps(..., indent=2)``,
  identical to the legacy behaviour. The ``ab``/``abs`` CLIs surface this
  via the ``--json`` flag.

Models opt into pretty rendering by defining ``cli_format()``. Anything
without it falls back to JSON.
"""

from __future__ import annotations

import json
from typing import Any


def _has_pretty(obj: Any) -> bool:
    return callable(getattr(obj, "cli_format", None))


def format_result(result: Any, *, as_json: bool = False) -> str:
    """Format an API response for stdout output.

    Args:
        result: The endpoint return value (Pydantic model, list, dict, primitive).
        as_json: Force JSON output regardless of whether ``cli_format`` is defined.
    """
    from pydantic import BaseModel

    if result is None:
        return "null"

    if isinstance(result, bytes):
        return f"<binary response, {len(result)} bytes>"

    if isinstance(result, BaseModel):
        if not as_json and _has_pretty(result):
            return result.cli_format()
        return json.dumps(result.model_dump(by_alias=True, mode="json"), indent=2)

    if isinstance(result, list):
        if not as_json and result and all(_has_pretty(item) for item in result):
            return "\n".join(item.cli_format() for item in result)
        items: list[Any] = []
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
