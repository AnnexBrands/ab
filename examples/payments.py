"""Example: Payment operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

if __name__ == "__main__":
    job_id = "12345"

    # Get payment info
    payment = api.payments.get(job_id)
    print(f"Payment info for job {job_id}:")
    print(f"  Total: ${payment.total_amount}")
    print(f"  Balance due: ${payment.balance_due}")
    print(f"  Status: {payment.payment_status}")

    # List payment sources
    sources = api.payments.get_sources(job_id)
    print(f"\nPayment sources:")
    for src in sources:
        default_marker = "(default)" if src.is_default else ""
        print(f"  {src.type}: ****{src.last_four} {default_marker}")

    # Pay by stored source
    result = api.payments.pay_by_source(job_id, {"sourceId": "src_abc123"})
    result.raise_for_error()
    print("\nPayment processed successfully")
