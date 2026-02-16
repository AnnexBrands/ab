"""Company Setup API endpoints (26 routes).

Covers Calendar, Stripe External Accounts, Document Templates,
Grid/Setup Settings, Container Thickness, Planner, Material, and Truck
under /api/company/{companyId}/.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

# Calendar (4)
_GET_CALENDAR = Route("GET", "/company/{companyId}/calendar/{date}", response_model="CalendarDay")
_GET_CALENDAR_BASEINFO = Route("GET", "/company/{companyId}/calendar/{date}/baseinfo", response_model="CalendarBaseInfo")
_GET_CALENDAR_STARTOFDAY = Route("GET", "/company/{companyId}/calendar/{date}/startofday", response_model="CalendarTimeInfo")
_GET_CALENDAR_ENDOFDAY = Route("GET", "/company/{companyId}/calendar/{date}/endofday", response_model="CalendarTimeInfo")

# Stripe External Accounts (3)
_GET_STRIPE_CONNECT_URL = Route("GET", "/company/{companyId}/accounts/stripe/connecturl", response_model="StripeConnectUrl")
_POST_STRIPE_COMPLETE = Route("POST", "/company/{companyId}/accounts/stripe/completeconnection", request_model="StripeCompleteRequest", response_model="StripeConnection")
_DELETE_STRIPE = Route("DELETE", "/company/{companyId}/accounts/stripe")

# Document Templates (4)
_GET_DOC_TEMPLATES = Route("GET", "/company/{companyId}/document-templates", response_model="List[DocumentTemplate]")
_POST_DOC_TEMPLATE = Route("POST", "/company/{companyId}/document-templates", request_model="DocumentTemplateRequest", response_model="DocumentTemplate")
_PUT_DOC_TEMPLATE = Route("PUT", "/company/{companyId}/document-templates/{documentId}", request_model="DocumentTemplateRequest", response_model="DocumentTemplate")
_DELETE_DOC_TEMPLATE = Route("DELETE", "/company/{companyId}/document-templates/{documentId}")

# Grid/Setup Settings (3)
_GET_GRID_SETTINGS = Route("GET", "/company/{companyId}/gridsettings", response_model="GridSettings")
_POST_GRID_SETTINGS = Route("POST", "/company/{companyId}/gridsettings", request_model="GridSettingsRequest", response_model="GridSettings")
_GET_SETUP_DATA = Route("GET", "/company/{companyId}/setupdata", response_model="CompanySetupData")

# Container Thickness (3)
_GET_CONTAINER_THICKNESS = Route("GET", "/company/{companyId}/containerthicknessinches", response_model="List[ContainerThickness]")
_POST_CONTAINER_THICKNESS = Route("POST", "/company/{companyId}/containerthicknessinches", request_model="ContainerThicknessRequest", response_model="ContainerThickness")
_DELETE_CONTAINER_THICKNESS = Route("DELETE", "/company/{companyId}/containerthicknessinches")

# Planner (1)
_GET_PLANNER = Route("GET", "/company/{companyId}/planner", response_model="List[PlannerEntry]")

# Material (4) — added in US5
_GET_MATERIALS = Route("GET", "/company/{companyId}/material", response_model="List[Material]")
_POST_MATERIAL = Route("POST", "/company/{companyId}/material", request_model="MaterialRequest", response_model="Material")
_PUT_MATERIAL = Route("PUT", "/company/{companyId}/material/{materialId}", request_model="MaterialRequest", response_model="Material")
_DELETE_MATERIAL = Route("DELETE", "/company/{companyId}/material/{materialId}")

# Truck (4) — added in US5
_GET_TRUCKS = Route("GET", "/company/{companyId}/truck", response_model="List[Truck]")
_POST_TRUCK = Route("POST", "/company/{companyId}/truck", request_model="TruckRequest", response_model="Truck")
_PUT_TRUCK = Route("PUT", "/company/{companyId}/truck/{truckId}", request_model="TruckRequest", response_model="Truck")
_DELETE_TRUCK = Route("DELETE", "/company/{companyId}/truck/{truckId}")


class CompanySetupEndpoint(BaseEndpoint):
    """Company setup operations (ACPortal API).

    Manages per-company configuration: calendar, Stripe accounts,
    document templates, grid settings, container thickness, planner,
    materials, and trucks.
    """

    # ---- Calendar -----------------------------------------------------------

    def get_calendar(self, company_id: str, date: str) -> Any:
        """GET /company/{companyId}/calendar/{date}"""
        return self._request(_GET_CALENDAR.bind(companyId=company_id, date=date))

    def get_calendar_baseinfo(self, company_id: str, date: str) -> Any:
        """GET /company/{companyId}/calendar/{date}/baseinfo"""
        return self._request(_GET_CALENDAR_BASEINFO.bind(companyId=company_id, date=date))

    def get_calendar_startofday(self, company_id: str, date: str) -> Any:
        """GET /company/{companyId}/calendar/{date}/startofday"""
        return self._request(_GET_CALENDAR_STARTOFDAY.bind(companyId=company_id, date=date))

    def get_calendar_endofday(self, company_id: str, date: str) -> Any:
        """GET /company/{companyId}/calendar/{date}/endofday"""
        return self._request(_GET_CALENDAR_ENDOFDAY.bind(companyId=company_id, date=date))

    # ---- Stripe External Accounts -------------------------------------------

    def get_stripe_connect_url(self, company_id: str, **params: Any) -> Any:
        """GET /company/{companyId}/accounts/stripe/connecturl"""
        return self._request(_GET_STRIPE_CONNECT_URL.bind(companyId=company_id), params=params or None)

    def complete_stripe_connection(self, company_id: str, **kwargs: Any) -> Any:
        """POST /company/{companyId}/accounts/stripe/completeconnection"""
        return self._request(_POST_STRIPE_COMPLETE.bind(companyId=company_id), json=kwargs)

    def delete_stripe(self, company_id: str) -> Any:
        """DELETE /company/{companyId}/accounts/stripe"""
        return self._request(_DELETE_STRIPE.bind(companyId=company_id))

    # ---- Document Templates -------------------------------------------------

    def get_document_templates(self, company_id: str) -> Any:
        """GET /company/{companyId}/document-templates"""
        return self._request(_GET_DOC_TEMPLATES.bind(companyId=company_id))

    def create_document_template(self, company_id: str, **kwargs: Any) -> Any:
        """POST /company/{companyId}/document-templates"""
        return self._request(_POST_DOC_TEMPLATE.bind(companyId=company_id), json=kwargs)

    def update_document_template(self, company_id: str, document_id: str, **kwargs: Any) -> Any:
        """PUT /company/{companyId}/document-templates/{documentId}"""
        return self._request(_PUT_DOC_TEMPLATE.bind(companyId=company_id, documentId=document_id), json=kwargs)

    def delete_document_template(self, company_id: str, document_id: str) -> Any:
        """DELETE /company/{companyId}/document-templates/{documentId}"""
        return self._request(_DELETE_DOC_TEMPLATE.bind(companyId=company_id, documentId=document_id))

    # ---- Grid/Setup Settings ------------------------------------------------

    def get_grid_settings(self, company_id: str) -> Any:
        """GET /company/{companyId}/gridsettings"""
        return self._request(_GET_GRID_SETTINGS.bind(companyId=company_id))

    def save_grid_settings(self, company_id: str, **kwargs: Any) -> Any:
        """POST /company/{companyId}/gridsettings"""
        return self._request(_POST_GRID_SETTINGS.bind(companyId=company_id), json=kwargs)

    def get_setup_data(self, company_id: str) -> Any:
        """GET /company/{companyId}/setupdata"""
        return self._request(_GET_SETUP_DATA.bind(companyId=company_id))

    # ---- Container Thickness ------------------------------------------------

    def get_container_thickness(self, company_id: str) -> Any:
        """GET /company/{companyId}/containerthicknessinches"""
        return self._request(_GET_CONTAINER_THICKNESS.bind(companyId=company_id))

    def create_container_thickness(self, company_id: str, **kwargs: Any) -> Any:
        """POST /company/{companyId}/containerthicknessinches"""
        return self._request(_POST_CONTAINER_THICKNESS.bind(companyId=company_id), json=kwargs)

    def delete_container_thickness(self, company_id: str, **params: Any) -> Any:
        """DELETE /company/{companyId}/containerthicknessinches — uses containerId query param."""
        return self._request(_DELETE_CONTAINER_THICKNESS.bind(companyId=company_id), params=params or None)

    # ---- Planner ------------------------------------------------------------

    def get_planner(self, company_id: str) -> Any:
        """GET /company/{companyId}/planner"""
        return self._request(_GET_PLANNER.bind(companyId=company_id))

    # ---- Material -----------------------------------------------------------

    def get_materials(self, company_id: str) -> Any:
        """GET /company/{companyId}/material"""
        return self._request(_GET_MATERIALS.bind(companyId=company_id))

    def create_material(self, company_id: str, **kwargs: Any) -> Any:
        """POST /company/{companyId}/material"""
        return self._request(_POST_MATERIAL.bind(companyId=company_id), json=kwargs)

    def update_material(self, company_id: str, material_id: str, **kwargs: Any) -> Any:
        """PUT /company/{companyId}/material/{materialId}"""
        return self._request(_PUT_MATERIAL.bind(companyId=company_id, materialId=material_id), json=kwargs)

    def delete_material(self, company_id: str, material_id: str) -> Any:
        """DELETE /company/{companyId}/material/{materialId}"""
        return self._request(_DELETE_MATERIAL.bind(companyId=company_id, materialId=material_id))

    # ---- Truck --------------------------------------------------------------

    def get_trucks(self, company_id: str, **params: Any) -> Any:
        """GET /company/{companyId}/truck — accepts onlyOwnTrucks query param."""
        return self._request(_GET_TRUCKS.bind(companyId=company_id), params=params or None)

    def create_truck(self, company_id: str, **kwargs: Any) -> Any:
        """POST /company/{companyId}/truck"""
        return self._request(_POST_TRUCK.bind(companyId=company_id), json=kwargs)

    def update_truck(self, company_id: str, truck_id: str, **kwargs: Any) -> Any:
        """PUT /company/{companyId}/truck/{truckId}"""
        return self._request(_PUT_TRUCK.bind(companyId=company_id, truckId=truck_id), json=kwargs)

    def delete_truck(self, company_id: str, truck_id: str) -> Any:
        """DELETE /company/{companyId}/truck/{truckId}"""
        return self._request(_DELETE_TRUCK.bind(companyId=company_id, truckId=truck_id))
