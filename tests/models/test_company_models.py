"""Fixture validation tests for Company models (T059)."""

import pytest

from tests.conftest import load_fixture

from ab.api.models.companies import CompanyDetails, CompanySimple, SearchCompanyResponse


class TestCompanyModels:
    @pytest.mark.live
    def test_company_simple(self):
        data = load_fixture("CompanySimple")
        model = CompanySimple.model_validate(data)
        assert model.id is not None
        assert model.name is not None

    @pytest.mark.live
    def test_company_details(self):
        data = load_fixture("CompanyDetails")
        model = CompanyDetails.model_validate(data)
        assert model.id is not None or model.details is not None

    @pytest.mark.mock
    def test_search_company_response(self):
        data = load_fixture("SearchCompanyResponse")
        model = SearchCompanyResponse.model_validate(data)
        assert model.id is not None
