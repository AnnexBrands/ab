"""Example: Shipment operations - rates, booking, and accessorials."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

if __name__ == "__main__":
    job_id = "12345"

    # Get rate quotes
    quotes = api.shipments.get_rate_quotes(job_id)
    print(f"Rate quotes for job {job_id}:")
    for quote in quotes:
        print(f"  {quote.carrier_name}: ${quote.total_charge} ({quote.transit_days} days)")

    # Book a shipment
    result = api.shipments.book(job_id, {
        "providerOptionIndex": 0,
        "shipDate": "2026-03-01",
    })
    result.raise_for_error()
    print("\nShipment booked successfully")

    # Get accessorials
    accessorials = api.shipments.get_accessorials(job_id)
    print(f"\nAccessorials for job {job_id}:")
    for acc in accessorials:
        print(f"  {acc.name}: ${acc.price}")

    # Get origin/destination
    od = api.shipments.get_origin_destination(job_id)
    print(f"\nOrigin: {od.origin}")
    print(f"Destination: {od.destination}")
