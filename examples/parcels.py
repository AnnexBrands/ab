"""Example: Parcel item operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

if __name__ == "__main__":
    job_id = "12345"

    # List parcel items
    parcels = api.jobs.list_parcel_items(job_id)
    print(f"Parcel items for job {job_id}:")
    for p in parcels:
        print(f"  {p.description}: {p.length}x{p.width}x{p.height} ({p.weight} lbs)")

    # Create a parcel item
    new_parcel = api.jobs.create_parcel_item(job_id, {
        "description": "Antique dresser",
        "length": 48,
        "width": 24,
        "height": 36,
        "weight": 150,
        "quantity": 1,
    })
    print(f"\nParcel created: {new_parcel.parcel_item_id}")

    # Get items with materials
    items_with_materials = api.jobs.get_parcel_items_with_materials(job_id)
    print(f"\nParcel items with materials:")
    for item in items_with_materials:
        material_count = len(item.materials or [])
        print(f"  {item.description}: {material_count} materials")
