"""Base endpoint class with instance-level HttpClient injection."""

from __future__ import annotations

import re
import logging
from typing import Any, Optional, Tuple, Type

from ab.api.route import Route
from ab.http import HttpClient

logger = logging.getLogger(__name__)

_LIST_RE = re.compile(r"^List\[(\w+)]$")


class BaseEndpoint:
    """Base class for all endpoint groups.

    Each endpoint receives its own :class:`~ab.http.HttpClient` instance
    (per D3 — instance-level injection, not class-level).
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_model(self, name: str) -> Type:
        """Lazily resolve a model name string to its class."""
        from ab.api import models

        is_list, inner = self._parse_type_string(name)
        cls = getattr(models, inner)
        return cls

    @staticmethod
    def _parse_type_string(type_str: str) -> Tuple[bool, str]:
        m = _LIST_RE.match(type_str)
        if m:
            return True, m.group(1)
        return False, type_str

    def _request(self, route: Route, **kwargs: Any) -> Any:
        """Dispatch a :class:`Route` through the HTTP client.

        Handles:
        - request model validation (if route.request_model is set and
          ``json`` is in kwargs)
        - response model casting (single or ``List[Model]``)
        """
        # Validate outbound body
        if "json" in kwargs and route.request_model:
            model_cls = self._resolve_model(route.request_model)
            body = kwargs["json"]
            if hasattr(model_cls, "check"):
                kwargs["json"] = model_cls.check(body)

        response = self._client.request(route.method, route.path, **kwargs)

        # Cast response to model(s)
        if route.response_model is None:
            return response

        if route.response_model == "bytes":
            return response

        is_list, model_name = self._parse_type_string(route.response_model)

        # Primitive types
        if model_name in ("str", "int", "bool"):
            return response

        model_cls = self._resolve_model(model_name)

        if is_list:
            if isinstance(response, list):
                return [model_cls.model_validate(item) for item in response]
            return response
        else:
            return model_cls.model_validate(response)

    def _paginated_request(self, route: Route, item_model: str, **kwargs: Any) -> Any:
        """Dispatch a route expecting a PaginatedList response."""
        from ab.api.models.shared import PaginatedList

        response = self._client.request(route.method, route.path, **kwargs)
        if response is None:
            return None

        model_cls = self._resolve_model(item_model)
        items = [model_cls.model_validate(item) for item in response.get("items", [])]

        return PaginatedList(
            items=items,
            page_number=response.get("pageNumber", 0),
            total_pages=response.get("totalPages", 0),
            total_items=response.get("totalItems", 0),
            has_previous_page=response.get("hasPreviousPage", False),
            has_next_page=response.get("hasNextPage", False),
        )
