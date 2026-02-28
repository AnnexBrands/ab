"""Shared response and request models used across multiple endpoints."""

from __future__ import annotations

import logging
from typing import Generic, List, Optional, TypeVar

from pydantic import Field

from ab.api.models.base import ResponseModel
from ab.api.models.mixins import PaginatedRequestMixin, SortableRequestMixin

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ServiceBaseResponse(ResponseModel):
    """Standard success/error wrapper returned by many ABConnect endpoints.

    Supports boolean evaluation::

        resp = api.some_endpoint(...)
        if resp:
            print("Success")
        else:
            resp.raise_for_error()
    """

    success: Optional[bool] = Field(None, description="Whether the operation succeeded")
    error_message: Optional[str] = Field(None, alias="errorMessage", description="Error detail when success is False")

    def raise_for_error(self) -> None:
        """Raise ``ValueError`` when ``success`` is ``False``."""
        if self.success is False:
            error_msg = self.error_message or "Unknown error"
            logger.error("API request failed: %s", error_msg)
            raise ValueError(error_msg)

    def __bool__(self) -> bool:
        return self.success is True


class ServiceWarningResponse(ServiceBaseResponse):
    """Extends :class:`ServiceBaseResponse` with an optional warning."""

    warning_message: Optional[str] = Field(
        None, alias="warningMessage", description="Warning present even on success"
    )

    def raise_for_error(self) -> None:
        if self.warning_message:
            logger.warning("API response warning: %s", self.warning_message)
        super().raise_for_error()


class PaginatedList(ResponseModel, Generic[T]):
    """Generic pagination wrapper used by the Catalog API.

    Example::

        result: PaginatedList[CatalogExpandedDto] = api.catalog.list(page=1)
        for item in result.items:
            print(item.title)
    """

    items: List[T] = Field(default_factory=list, description="Page of results")
    page_number: int = Field(0, alias="pageNumber", description="Current page (1-based)")
    total_pages: int = Field(0, alias="totalPages", description="Total pages available")
    total_items: int = Field(0, alias="totalItems", description="Total items across all pages")
    has_previous_page: bool = Field(False, alias="hasPreviousPage")
    has_next_page: bool = Field(False, alias="hasNextPage")


class ListRequest(PaginatedRequestMixin, SortableRequestMixin):
    """Shared request body for paginated list endpoints (Companies, Users)."""

    filters: Optional[dict] = Field(None, description="Filter criteria")
