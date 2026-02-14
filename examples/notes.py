"""Example: Job notes operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

if __name__ == "__main__":
    job_id = "12345"

    # List notes for a job
    notes = api.jobs.list_notes(job_id)
    print(f"Notes for job {job_id}:")
    for note in notes:
        print(f"  [{note.author}] {note.comment}")

    # Create a note
    new_note = api.jobs.create_note(job_id, {
        "comments": "Customer called about delivery window",
        "taskCode": "SCH",
        "isImportant": True,
        "sendNotification": True,
    })
    print(f"\nNote created: {new_note.id}")
