"""Job-scoped email operations — swagger tag ``JobEmail`` (4 routes).

Exposed as ``api.jobs.email``. Old names on
:class:`~ab.api.endpoints.jobs.JobsEndpoint` remain as deprecation shims.

Method renames (``_email`` suffix dropped):

* :meth:`send`                  (was ``send_email``)
* :meth:`send_document`         (was ``send_document_email``)
* :meth:`create_transactional`  (was ``create_transactional_email``)
* :meth:`send_template`         (was ``send_template_email``)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.jobs import SendDocumentEmailModel, SendEmailRequest

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_SEND = Route("POST", "/job/{jobDisplayId}/email", request_model="SendEmailRequest")
_SEND_DOCUMENT = Route(
    "POST",
    "/job/{jobDisplayId}/email/senddocument",
    request_model="SendDocumentEmailModel",
)
_CREATE_TRANSACTIONAL = Route("POST", "/job/{jobDisplayId}/email/createtransactionalemail")
_SEND_TEMPLATE = Route("POST", "/job/{jobDisplayId}/email/{emailTemplateGuid}/send")


class JobEmailEndpoint(BaseEndpoint):
    """Job-scoped email operations (ACPortal API)."""

    def send(self, job_display_id: int, *, data: SendEmailRequest | dict) -> None:
        """``POST /job/{jobDisplayId}/email``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/email.send.html
        Request model: SendEmailRequest
        """
        return self._request(_SEND.bind(jobDisplayId=job_display_id), json=data)

    def send_document(
        self,
        job_display_id: int,
        *,
        data: SendDocumentEmailModel | dict,
    ) -> None:
        """``POST /job/{jobDisplayId}/email/senddocument``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/email.send_document.html
        Request model: SendDocumentEmailModel
        """
        return self._request(_SEND_DOCUMENT.bind(jobDisplayId=job_display_id), json=data)

    def create_transactional(self, job_display_id: int) -> None:
        """``POST /job/{jobDisplayId}/email/createtransactionalemail``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/email.create_transactional.html
        """
        return self._request(_CREATE_TRANSACTIONAL.bind(jobDisplayId=job_display_id))

    def send_template(self, job_display_id: int, template_guid: str) -> None:
        """``POST /job/{jobDisplayId}/email/{emailTemplateGuid}/send``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/email.send_template.html
        """
        return self._request(
            _SEND_TEMPLATE.bind(jobDisplayId=job_display_id, emailTemplateGuid=template_guid),
        )
