"""Standalone pagination helper for iterating through paginated list endpoints."""

from __future__ import annotations

from typing import Any, Callable, Generator, TypeVar

from ab.api.models.shared import PaginatedList

T = TypeVar("T")


def paginate(
    list_fn: Callable[..., PaginatedList[T]],
    **kwargs: Any,
) -> Generator[PaginatedList[T], None, None]:
    """Yield successive pages from a paginated list endpoint.

    Args:
        list_fn: A bound list method (e.g. ``api.catalog.list``).
        **kwargs: Filter and pagination keyword arguments forwarded to
            *list_fn*.  ``page_number`` is managed automatically and
            should not be passed.

    Yields:
        Each :class:`PaginatedList` page in order until the last page.

    Example::

        from ab import ABConnectAPI, paginate

        api = ABConnectAPI()
        for page in paginate(api.catalog.list, page_size=10):
            for item in page.items:
                print(item.title)
    """
    page_number = kwargs.pop("page_number", 1)
    while True:
        result = list_fn(page_number=page_number, **kwargs)
        if result is None:
            return
        yield result
        if not result.has_next_page:
            return
        page_number += 1
