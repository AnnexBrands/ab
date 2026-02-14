"""Example: Job timeline and status operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

if __name__ == "__main__":
    job_id = "12345"

    # Get timeline for a job
    tasks = api.jobs.get_timeline(job_id)
    print(f"Timeline tasks for job {job_id}:")
    for task in tasks:
        print(f"  {task.task_code}: {task.status_name} (scheduled: {task.scheduled_date})")

    # Create a timeline task
    new_task = api.jobs.create_timeline_task(job_id, {
        "taskCode": "SCH",
        "scheduledDate": "2026-03-01T09:00:00",
        "comments": "Scheduled for pickup",
    })
    print(f"\nCreated task: {new_task.id}")

    # Increment job status
    result = api.jobs.increment_status(job_id)
    result.raise_for_error()
    print("\nJob status advanced")

    # Optionally undo
    # undo_result = api.jobs.undo_increment_status(job_id)
    # undo_result.raise_for_error()
    # print("Status reverted")
