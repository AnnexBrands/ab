from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

job = 1913494

tasks = api.jobs.get_timeline(job)

print(tasks)
