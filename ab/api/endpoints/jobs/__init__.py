"""Jobs endpoint subpackage.

Top-level public class: :class:`JobsEndpoint` (re-exported here).

Subgroups (each is a :class:`~ab.api.base.BaseEndpoint` instance attached
to a :class:`JobsEndpoint` and named for its swagger tag, lowercased
with ``Job`` stripped and snake_case applied to multi-word tags):

* :attr:`JobsEndpoint.note`     — JobNote      (``ab.api.endpoints.jobs.note.JobNoteEndpoint``)
* :attr:`JobsEndpoint.on_hold`  — JobOnHold    (``ab.api.endpoints.jobs.on_hold.JobOnHoldEndpoint``)
* :attr:`JobsEndpoint.form`     — JobForm      (``ab.api.endpoints.jobs.form.JobFormEndpoint``)
"""

from ab.api.endpoints.jobs._main import JobsEndpoint
from ab.api.endpoints.jobs.email import JobEmailEndpoint
from ab.api.endpoints.jobs.form import JobFormEndpoint
from ab.api.endpoints.jobs.freight_providers import JobFreightProvidersEndpoint
from ab.api.endpoints.jobs.note import JobNoteEndpoint
from ab.api.endpoints.jobs.on_hold import JobOnHoldEndpoint
from ab.api.endpoints.jobs.parcel_items import JobParcelItemsEndpoint
from ab.api.endpoints.jobs.payment import JobPaymentEndpoint
from ab.api.endpoints.jobs.rfq import JobRfqEndpoint
from ab.api.endpoints.jobs.shipment import JobShipmentEndpoint
from ab.api.endpoints.jobs.sms import JobSmsEndpoint
from ab.api.endpoints.jobs.status import JobStatusEndpoint
from ab.api.endpoints.jobs.timeline import JobTimelineEndpoint
from ab.api.endpoints.jobs.tracking import JobTrackingEndpoint

__all__ = [
    "JobsEndpoint",
    "JobNoteEndpoint",
    "JobOnHoldEndpoint",
    "JobFormEndpoint",
    "JobTimelineEndpoint",
    "JobEmailEndpoint",
    "JobSmsEndpoint",
    "JobFreightProvidersEndpoint",
    "JobParcelItemsEndpoint",
    "JobTrackingEndpoint",
    "JobStatusEndpoint",
    "JobPaymentEndpoint",
    "JobShipmentEndpoint",
    "JobRfqEndpoint",
]
