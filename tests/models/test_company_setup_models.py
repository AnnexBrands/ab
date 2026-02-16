"""Fixture validation tests for Company Setup models (009)."""

from tests.conftest import require_fixture

from ab.api.models.company_setup import (
    CalendarBaseInfo,
    CalendarDay,
    CalendarTimeInfo,
    CompanySetupData,
    ContainerThickness,
    DocumentTemplate,
    GridSettings,
    Material,
    PlannerEntry,
    StripeConnectUrl,
    StripeConnection,
    Truck,
)


class TestCompanySetupModels:
    # ---- Calendar -----------------------------------------------------------

    def test_calendar_day(self):
        data = require_fixture("CalendarDay", "GET", "/company/{id}/calendar/{date}")
        CalendarDay.model_validate(data)

    def test_calendar_base_info(self):
        data = require_fixture("CalendarBaseInfo", "GET", "/company/{id}/calendar/{date}/baseinfo")
        CalendarBaseInfo.model_validate(data)

    def test_calendar_time_info_start(self):
        data = require_fixture("CalendarTimeInfo", "GET", "/company/{id}/calendar/{date}/startofday")
        CalendarTimeInfo.model_validate(data)

    # ---- Stripe External Accounts -------------------------------------------

    def test_stripe_connect_url(self):
        data = require_fixture("StripeConnectUrl", "GET", "/company/{id}/accounts/stripe/connecturl")
        StripeConnectUrl.model_validate(data)

    def test_stripe_connection(self):
        data = require_fixture("StripeConnection", "POST", "/company/{id}/accounts/stripe/completeconnection")
        StripeConnection.model_validate(data)

    # ---- Document Templates -------------------------------------------------

    def test_document_template(self):
        data = require_fixture("DocumentTemplate", "GET", "/company/{id}/document-templates")
        DocumentTemplate.model_validate(data)

    # ---- Grid/Setup Settings ------------------------------------------------

    def test_grid_settings(self):
        data = require_fixture("GridSettings", "GET", "/company/{id}/gridsettings")
        GridSettings.model_validate(data)

    def test_company_setup_data(self):
        data = require_fixture("CompanySetupData", "GET", "/company/{id}/setupdata")
        CompanySetupData.model_validate(data)

    # ---- Container Thickness ------------------------------------------------

    def test_container_thickness(self):
        data = require_fixture("ContainerThickness", "GET", "/company/{id}/containerthicknessinches")
        ContainerThickness.model_validate(data)

    # ---- Planner ------------------------------------------------------------

    def test_planner_entry(self):
        data = require_fixture("PlannerEntry", "GET", "/company/{id}/planner")
        PlannerEntry.model_validate(data)

    # ---- Material -----------------------------------------------------------

    def test_material(self):
        data = require_fixture("Material", "GET", "/company/{id}/material")
        Material.model_validate(data)

    # ---- Truck --------------------------------------------------------------

    def test_truck(self):
        data = require_fixture("Truck", "GET", "/company/{id}/truck")
        Truck.model_validate(data)
