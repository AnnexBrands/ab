"""Enforce that every RequestModel field has a non-empty description.

This test iterates all RequestModel subclasses exported from ab.api.models
and checks that every field has a ``description`` in its ``Field()`` declaration.
"""

from __future__ import annotations

import pytest

from ab.api.models.base import RequestModel
import ab.api.models as models_pkg


def _all_request_models() -> list[type]:
    """Collect every RequestModel subclass exported from ab.api.models."""
    result = []
    for name in dir(models_pkg):
        obj = getattr(models_pkg, name)
        if (
            isinstance(obj, type)
            and issubclass(obj, RequestModel)
            and obj is not RequestModel
        ):
            result.append(obj)
    return sorted(result, key=lambda c: c.__name__)


def _fields_missing_descriptions(model_cls: type) -> list[str]:
    """Return field names that lack a non-empty description."""
    missing = []
    for field_name, field_info in model_cls.model_fields.items():
        desc = field_info.description
        if not desc or not desc.strip():
            missing.append(field_name)
    return missing


_REQUEST_MODELS = _all_request_models()


@pytest.mark.parametrize(
    "model_cls",
    _REQUEST_MODELS,
    ids=lambda c: c.__name__,
)
def test_request_model_fields_have_descriptions(model_cls: type) -> None:
    """Every field in a RequestModel subclass must have a description."""
    missing = _fields_missing_descriptions(model_cls)
    assert not missing, (
        f"{model_cls.__name__} has fields without descriptions: {missing}"
    )
