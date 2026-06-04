from ab import ABConnectAPI


def main() -> None:
    api = ABConnectAPI()

    job = 1913494

    result = api.jobs.tasks.schedule(job, "2026-06-01T10:00:00Z", "2026-06-01T12:00:00Z")
    print(result)

    tasks = api.jobs.timeline.list(job)
    print(tasks)

    # notes = api.jobs.note.list(job)
    # print(notes)


if __name__ == "__main__":
    main()
