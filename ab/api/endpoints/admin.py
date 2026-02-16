"""Admin API endpoints (13 routes).

Covers AdvancedSettings, CarrierErrorMessage, GlobalSettings,
and LogBuffer under /api/admin/.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

# AdvancedSettings (4)
_GET_ADVANCED_SETTINGS_ALL = Route("GET", "/admin/advancedsettings/all", response_model="List[AdvancedSetting]")
_GET_ADVANCED_SETTING = Route("GET", "/admin/advancedsettings/{id}", response_model="AdvancedSetting")
_POST_ADVANCED_SETTING = Route("POST", "/admin/advancedsettings", request_model="AdvancedSettingRequest", response_model="AdvancedSetting")
_DELETE_ADVANCED_SETTING = Route("DELETE", "/admin/advancedsettings/{id}")

# CarrierErrorMessage (2)
_GET_CARRIER_ERRORS_ALL = Route("GET", "/admin/carriererrormessage/all", response_model="List[CarrierErrorMessage]")
_POST_CARRIER_ERROR = Route("POST", "/admin/carriererrormessage", request_model="CarrierErrorMessageRequest", response_model="CarrierErrorMessage")

# GlobalSettings (5)
_GET_COMPANY_HIERARCHY = Route("GET", "/admin/globalsettings/companyhierarchy", response_model="CompanyHierarchy")
_GET_COMPANY_HIERARCHY_BY_ID = Route("GET", "/admin/globalsettings/companyhierarchy/company/{companyId}", response_model="CompanyHierarchy")
_POST_INSURANCE_EXCEPTIONS = Route("POST", "/admin/globalsettings/getinsuranceexceptions", request_model="InsuranceExceptionFilter", response_model="List[InsuranceException]")
_POST_APPROVE_INSURANCE = Route("POST", "/admin/globalsettings/approveinsuranceexception")
_POST_INTACCT_SETTINGS = Route("POST", "/admin/globalsettings/intacct", request_model="IntacctSettingsRequest", response_model="IntacctSettings")

# LogBuffer (2)
_POST_LOG_FLUSH = Route("POST", "/admin/logbuffer/flush", request_model="LogFlushRequest")
_POST_LOG_FLUSH_ALL = Route("POST", "/admin/logbuffer/flushAll")


class AdminEndpoint(BaseEndpoint):
    """Admin operations (ACPortal API).

    Manages advanced settings, carrier error messages, global settings
    (company hierarchy, insurance exceptions, Intacct), and log buffer.
    """

    # ---- Advanced Settings --------------------------------------------------

    def get_advanced_settings(self) -> Any:
        """GET /admin/advancedsettings/all"""
        return self._request(_GET_ADVANCED_SETTINGS_ALL)

    def get_advanced_setting(self, setting_id: str) -> Any:
        """GET /admin/advancedsettings/{id}"""
        return self._request(_GET_ADVANCED_SETTING.bind(id=setting_id))

    def create_advanced_setting(self, **kwargs: Any) -> Any:
        """POST /admin/advancedsettings"""
        return self._request(_POST_ADVANCED_SETTING, json=kwargs)

    def delete_advanced_setting(self, setting_id: str) -> Any:
        """DELETE /admin/advancedsettings/{id}"""
        return self._request(_DELETE_ADVANCED_SETTING.bind(id=setting_id))

    # ---- Carrier Error Messages ---------------------------------------------

    def get_carrier_error_messages(self) -> Any:
        """GET /admin/carriererrormessage/all"""
        return self._request(_GET_CARRIER_ERRORS_ALL)

    def create_carrier_error_message(self, **kwargs: Any) -> Any:
        """POST /admin/carriererrormessage"""
        return self._request(_POST_CARRIER_ERROR, json=kwargs)

    # ---- Global Settings ----------------------------------------------------

    def get_company_hierarchy(self) -> Any:
        """GET /admin/globalsettings/companyhierarchy"""
        return self._request(_GET_COMPANY_HIERARCHY)

    def get_company_hierarchy_by_id(self, company_id: str) -> Any:
        """GET /admin/globalsettings/companyhierarchy/company/{companyId}"""
        return self._request(_GET_COMPANY_HIERARCHY_BY_ID.bind(companyId=company_id))

    def get_insurance_exceptions(self, **kwargs: Any) -> Any:
        """POST /admin/globalsettings/getinsuranceexceptions"""
        return self._request(_POST_INSURANCE_EXCEPTIONS, json=kwargs)

    def approve_insurance_exception(self, **params: Any) -> Any:
        """POST /admin/globalsettings/approveinsuranceexception — uses JobId query param."""
        return self._request(_POST_APPROVE_INSURANCE, params=params or None)

    def save_intacct_settings(self, **kwargs: Any) -> Any:
        """POST /admin/globalsettings/intacct"""
        return self._request(_POST_INTACCT_SETTINGS, json=kwargs)

    # ---- Log Buffer ---------------------------------------------------------

    def flush_log(self, **kwargs: Any) -> Any:
        """POST /admin/logbuffer/flush"""
        return self._request(_POST_LOG_FLUSH, json=kwargs or None)

    def flush_all_logs(self) -> Any:
        """POST /admin/logbuffer/flushAll"""
        return self._request(_POST_LOG_FLUSH_ALL)
