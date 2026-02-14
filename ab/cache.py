"""Cache-based code-to-UUID resolution (FR-012).

Provides a per-client in-memory cache that lazily resolves friendly
codes (e.g., CompanyCode ``"9999AZ"``) to their UUID equivalents via
an external lookup service.
"""

from __future__ import annotations

import logging
from typing import Dict, Optional

from ab.http import HttpClient

logger = logging.getLogger(__name__)

_CACHE_URL = "https://tasks.abconnect.co/cache/{key}"


class CodeResolver:
    """Resolves friendly codes to UUIDs using the ABConnect cache service.

    The resolver maintains an in-memory dict populated lazily on first
    lookup.  Cache is per-client-instance.
    """

    def __init__(self, client: HttpClient, api_secret: str) -> None:
        self._client = client
        self._api_secret = api_secret
        self._cache: Dict[str, str] = {}

    def resolve(self, code_or_uuid: str) -> str:
        """Return the UUID for *code_or_uuid*.

        If the value is already a UUID (contains ``-`` and is 36 chars)
        it is returned unchanged.  Otherwise the cache service is queried.
        """
        if self._looks_like_uuid(code_or_uuid):
            return code_or_uuid

        upper = code_or_uuid.upper()
        if upper in self._cache:
            return self._cache[upper]

        resolved = self._lookup(upper)
        if resolved:
            self._cache[upper] = resolved
            return resolved

        # Fall back — let the API decide
        return code_or_uuid

    def _lookup(self, key: str) -> Optional[str]:
        import requests as _requests

        url = _CACHE_URL.format(key=key)
        try:
            resp = _requests.get(url, headers={"x-api-key": self._api_secret}, timeout=10)
            if resp.ok and resp.text:
                return resp.text.strip()
        except Exception:
            logger.warning("Cache lookup failed for %s", key)
        return None

    @staticmethod
    def _looks_like_uuid(value: str) -> bool:
        return len(value) == 36 and value.count("-") == 4
