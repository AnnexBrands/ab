"""Unit tests for Route (T050)."""

from __future__ import annotations

import pytest

from ab.api.route import Route


class TestRoute:
    def test_route_is_frozen(self):
        r = Route("GET", "/companies/{id}")
        with pytest.raises(AttributeError):
            r.method = "POST"

    def test_bind_returns_new_instance(self):
        r = Route("GET", "/companies/{companyId}/details", response_model="CompanyDetails")
        bound = r.bind(companyId="abc-123")
        assert bound.path == "/companies/abc-123/details"
        assert r.path == "/companies/{companyId}/details"  # original unchanged
        assert bound is not r

    def test_bind_preserves_metadata(self):
        r = Route("PUT", "/catalog/{id}", request_model="UpdateCatalogRequest", response_model="CatalogWithSellersDto", api_surface="catalog")
        bound = r.bind(id="42")
        assert bound.method == "PUT"
        assert bound.request_model == "UpdateCatalogRequest"
        assert bound.response_model == "CatalogWithSellersDto"
        assert bound.api_surface == "catalog"

    def test_bind_multiple_params(self):
        r = Route("GET", "/companies/{companyId}/contacts/{contactId}")
        bound = r.bind(companyId="c1", contactId="c2")
        assert bound.path == "/companies/c1/contacts/c2"

    def test_default_api_surface(self):
        r = Route("GET", "/test")
        assert r.api_surface == "acportal"

    def test_string_model_resolution(self):
        r = Route("GET", "/test", response_model="CompanySimple")
        assert r.response_model == "CompanySimple"
        assert isinstance(r.response_model, str)
