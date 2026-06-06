"""Compare an example's produced output to its committed fixture (feature 037).

Single home for the comparison policy (research D3 / FR-009). Used by
``scripts/run_examples.py`` to decide ``passing`` vs ``failing``.

Policy:
- Normalize both sides by recursively dropping a documented set of *volatile* keys
  (per-request ids, server timestamps) plus any field whose name reads as a
  date/time. v1 drops dates outright (deterministic) rather than fuzzy-matching.
- Then require structural equality: dicts key-by-key, lists length-then-elementwise.
- On mismatch, return a compact unified diff of the normalized JSON (capped).
"""

from __future__ import annotations

import difflib
import json
import re
from typing import Any

#: Keys dropped anywhere in the tree before comparison (lower-cased, underscore-free).
VOLATILE_KEYS: set[str] = {
    "correlationid",
    "requestid",
    "traceid",
    "servertime",
    "timestamp",
}

# Date/time fields are matched on a real boundary — a camelCase suffix (capital D/T)
# or a snake ``_suffix`` — NOT a bare substring. This avoids silently dropping
# meaningful fields that merely end in those letters: ``allowJobInfoUpdate``,
# ``dontValidate``, ``runtime``, ``lifetime``, ``candidate`` (the UAT-era bug where a
# genuine mismatch was reported as a match).
_VOLATILE_CAMEL_RE = re.compile(r"(?:Date|DateTime|Timestamp|Ticks|Time|Utc)$")
_VOLATILE_SNAKE_RE = re.compile(r"(?:^|_)(?:date|datetime|timestamp|ticks|time|utc)$")

_MAX_DIFF_LINES = 40


def _is_volatile_key(key: str) -> bool:
    if key.replace("_", "").lower() in VOLATILE_KEYS:
        return True
    return bool(_VOLATILE_CAMEL_RE.search(key) or _VOLATILE_SNAKE_RE.search(key))


def normalize(obj: Any) -> Any:
    """Recursively drop volatile keys so stable structure can be compared."""
    if isinstance(obj, dict):
        return {
            k: normalize(v)
            for k, v in obj.items()
            if not _is_volatile_key(str(k))
        }
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    return obj


def _dumps(obj: Any) -> list[str]:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False).splitlines()


def compare(produced: Any, expected: Any) -> tuple[bool, str | None]:
    """Return ``(matches, detail)`` for produced vs expected (fixture) JSON.

    *detail* is ``None`` on a match, else a capped unified diff of the normalized
    representations.
    """
    np, ne = normalize(produced), normalize(expected)
    if np == ne:
        return True, None

    diff = list(
        difflib.unified_diff(_dumps(ne), _dumps(np), fromfile="fixture", tofile="produced", lineterm="")
    )
    if len(diff) > _MAX_DIFF_LINES:
        diff = diff[:_MAX_DIFF_LINES] + [f"... ({len(diff) - _MAX_DIFF_LINES} more diff lines)"]
    return False, "\n".join(diff)
