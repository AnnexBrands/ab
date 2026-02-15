"""Immutable Route dataclass with string-based lazy model resolution."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Route:
    """Describes a single API endpoint.

    Routes are **frozen** (immutable).  To bind path parameters, call
    :meth:`bind` which returns a *new* ``Route`` with the parameters applied.

    Model names are stored as **strings** and resolved lazily at request time
    via ``getattr(models, name)`` in :class:`~ab.api.base.BaseEndpoint`.
    """

    method: str
    path: str
    request_model: Optional[str] = None
    params_model: Optional[str] = None
    response_model: Optional[str] = None
    api_surface: str = "acportal"  # acportal | catalog | abc

    # Private: extracted ``{param}`` names — populated in __post_init__
    _path_params: frozenset[str] = field(default=frozenset(), repr=False, compare=False)

    def __post_init__(self) -> None:
        # frozen=True requires object.__setattr__ for post-init mutation
        names = frozenset(re.findall(r"\{([^}]+)\}", self.path))
        object.__setattr__(self, "_path_params", names)

    def bind(self, **params: str) -> Route:
        """Return a new ``Route`` with path parameters substituted.

        >>> r = Route("GET", "/companies/{companyId}/details")
        >>> bound = r.bind(companyId="abc-123")
        >>> bound.path
        '/companies/abc-123/details'
        """
        new_path = self.path
        for key, value in params.items():
            new_path = new_path.replace(f"{{{key}}}", str(value))
        return Route(
            method=self.method,
            path=new_path,
            request_model=self.request_model,
            params_model=self.params_model,
            response_model=self.response_model,
            api_surface=self.api_surface,
        )
