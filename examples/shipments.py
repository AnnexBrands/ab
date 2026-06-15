"""Example: Shipments operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_shipments.py) to the plain-script form.

Only the three non-job-scoped shipment routes live here; the job-scoped
operations have moved to ``api.jobs.shipment`` (see examples/jobs/).
All three calls are read-only GETs.

See also: https://ab-sdk.readthedocs.io/en/latest/api/shipments.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import save


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /shipment
    print("\n# api.shipments.get_shipment()")
    result = api.shipments.get_shipment()
    print(format_result(result))
    save("ShipmentInfo.json", result)

    # GET /shipment/accessorials
    print("\n# api.shipments.get_global_accessorials()")
    result = api.shipments.get_global_accessorials()
    print(format_result(result))
    save("GlobalAccessorial.json", result)

    # GET /shipment/document/{docId} — binary (PDF/image) response.
    print("\n# api.shipments.get_shipment_document(doc_id=...)")
    result = api.shipments.get_shipment_document("DOC_ID")  # staging document id
    print(f"  received {len(result)} bytes" if isinstance(result, bytes) else result)
    # Binary response — no JSON fixture to diff; save() would skip it, so we omit it.


if __name__ == "__main__":
    main()
