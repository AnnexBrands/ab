"""Job-scoped SMS operations — swagger tag ``JobSms`` (4 routes).

Exposed as ``api.jobs.sms``. Old names on
:class:`~ab.api.endpoints.jobs.JobsEndpoint` remain as deprecation shims.

Method renames (``_sms`` suffix dropped):

* :meth:`list`         (was ``list_sms``)
* :meth:`send`         (was ``send_sms``)
* :meth:`mark_read`    (was ``mark_sms_read``)
* :meth:`get_template` (was ``get_sms_template``)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.jobs import MarkSmsAsReadModel, SendSMSModel

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("GET", "/job/{jobDisplayId}/sms")
_SEND = Route("POST", "/job/{jobDisplayId}/sms", request_model="SendSMSModel")
_MARK_READ = Route("POST", "/job/{jobDisplayId}/sms/read", request_model="MarkSmsAsReadModel")
_GET_TEMPLATE = Route("GET", "/job/{jobDisplayId}/sms/templatebased/{templateId}")


class JobSmsEndpoint(BaseEndpoint):
    """Job-scoped SMS operations (ACPortal API)."""

    def list(self, job_display_id: int) -> None:
        """``GET /job/{jobDisplayId}/sms``"""
        return self._request(_LIST.bind(jobDisplayId=job_display_id))

    def send(self, job_display_id: int, *, data: SendSMSModel | dict) -> None:
        """``POST /job/{jobDisplayId}/sms``"""
        return self._request(_SEND.bind(jobDisplayId=job_display_id), json=data)

    def mark_read(self, job_display_id: int, *, data: MarkSmsAsReadModel | dict) -> None:
        """``POST /job/{jobDisplayId}/sms/read``"""
        return self._request(_MARK_READ.bind(jobDisplayId=job_display_id), json=data)

    def get_template(self, job_display_id: int, template_id: str) -> None:
        """``GET /job/{jobDisplayId}/sms/templatebased/{templateId}``"""
        return self._request(
            _GET_TEMPLATE.bind(jobDisplayId=job_display_id, templateId=template_id),
        )
