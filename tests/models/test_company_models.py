"""Fixture validation tests for Company models (T059)."""

import pytest

from tests.conftest import require_fixture

from ab.api.models.companies import CompanyDetails, CompanySimple, SearchCompanyResponse


class TestCompanyModels:
    @pytest.mark.live
    def test_company_simple(self):
        data = require_fixture("CompanySimple", "GET", "/companies/{id}")
        model = CompanySimple.model_validate(data)
        assert model.id is not None
        assert model.name is not None

    @pytest.mark.live
    def test_company_details(self):
        data = require_fixture("CompanyDetails", "GET", "/companies/{id}/fulldetails")
        model = CompanyDetails.model_validate(data)
        assert model.id is not None or model.details is not None

    @pytest.mark.live
    def test_search_company_response(self):
        data = require_fixture("SearchCompanyResponse", "GET", "/companies/availableByCurrentUser")
        model = SearchCompanyResponse.model_validate(data)
        assert model.id is not None
        assert model.company_name is not None
