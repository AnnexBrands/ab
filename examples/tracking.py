"""Example: Tracking operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

if __name__ == "__main__":
    job_id = "12345"

    # Get basic tracking info
    tracking = api.jobs.get_tracking(job_id)
    print(f"Tracking for job {job_id}:")
    print(f"  Status: {tracking.status}")
    print(f"  Location: {tracking.location}")
    print(f"  ETA: {tracking.estimated_delivery}")

    # Get v3 tracking with history
    tracking_v3 = api.jobs.get_tracking_v3(job_id, history_amount=10)
    print(f"\nTracking history (v3):")
    for detail in tracking_v3.tracking_details:
        print(f"  {detail}")
