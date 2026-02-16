"""Fixture validation tests for Intacct models (009)."""

from tests.conftest import require_fixture

from ab.api.models.intacct import JobIntacctData


class TestIntacctModels:
    def test_job_intacct_data(self):
        data = require_fixture("JobIntacctData", "GET", "/jobintacct/{jobDisplayId}")
        JobIntacctData.model_validate(data)
