"""Example: Forms generation - invoices, BOLs, and packing slips."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

if __name__ == "__main__":
    job_id = "12345"

    # Get invoice (bytes)
    invoice_pdf = api.forms.get_invoice(job_id)
    with open(f"invoice_{job_id}.pdf", "wb") as f:
        f.write(invoice_pdf)
    print(f"Invoice saved ({len(invoice_pdf)} bytes)")

    # Get bill of lading
    bol_pdf = api.forms.get_bill_of_lading(job_id)
    with open(f"bol_{job_id}.pdf", "wb") as f:
        f.write(bol_pdf)
    print(f"Bill of lading saved ({len(bol_pdf)} bytes)")

    # Get shipment plans (JSON)
    plans = api.forms.get_shipments(job_id)
    print(f"\nShipment plans for job {job_id}:")
    for plan in plans:
        print(f"  Plan {plan.shipment_plan_id}: {plan.carrier_name} ({plan.service_type})")

    # Generate BOL for specific plan
    if plans:
        specific_bol = api.forms.get_bill_of_lading(
            job_id,
            shipment_plan_id=plans[0].shipment_plan_id,
            provider_option_index=plans[0].provider_option_index
        )
        print(f"\nGenerated BOL for specific plan ({len(specific_bol)} bytes)")
