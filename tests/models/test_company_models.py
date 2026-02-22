"""Fixture validation tests for Company models."""

import pytest

from ab.api.models.companies import CompanyDetails, CompanySimple, SearchCompanyResponse
from tests.conftest import assert_no_extra_fields, require_fixture


class TestCompanyModels:
    @pytest.mark.live
    def test_company_simple(self):
        data = require_fixture("CompanySimple", "GET", "/companies/{id}", required=True)
        model = CompanySimple.model_validate(data)
        assert isinstance(model, CompanySimple)
        assert_no_extra_fields(model)
        assert model.id is not None

    @pytest.mark.live
    def test_company_details(self):
        data = require_fixture("CompanyDetails", "GET", "/companies/{id}/fulldetails", required=True)
        model = CompanyDetails.model_validate(data)
        assert isinstance(model, CompanyDetails)
        assert_no_extra_fields(model)
        assert model.id is not None
        assert model.details is not None

    @pytest.mark.live
    def test_search_company_response(self):
        data = require_fixture("SearchCompanyResponse", "GET", "/companies/availableByCurrentUser", required=True)
        if isinstance(data, list) and data:
            data = data[0]
        model = SearchCompanyResponse.model_validate(data)
        assert isinstance(model, SearchCompanyResponse)
        assert_no_extra_fields(model)
        assert model.id is not None
