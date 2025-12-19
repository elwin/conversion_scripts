import itertools
import multiprocessing
import os
import statistics
from tabulate import tabulate
import requests

pipeline_nums = 10
parallelism = 100

def average(lst):
    return sum(lst) / len(lst)


def median(lst):
    return statistics.median(lst)


token = os.getenv("GITLAB_TOKEN_RO")

# pool = multiprocessing.Pool(parallelism)

def main():
    project_ids = {
        34401392: "iot-data-provider",
        35505523: "fleet-ops",
        48079192: "nx0",
        16699974: "connect",
        9570796: "re-connect",
        23935579: "track-and-trace",
    }

    headers = ["project", "median", "average", "max"]
    table = []

    pool = multiprocessing.Pool()
    for (project_id, res) in pool.map(fetch_duration_wrapper, project_ids.keys()):
        durations = fetch_durations(project_id)
        table.append([project_ids[project_id], median(durations) / 60, average(durations) / 60, max(durations) / 60])

    print(tabulate(table, headers=headers, tablefmt="tsv"))


def fetch_duration_wrapper(project_id):
    return project_id, fetch_durations(project_id)


def fetch_durations(project_id):
    def get(url):
        return requests.get(url, headers={"PRIVATE-TOKEN": token})

    def get_pipelines():
        page = 1
        while True:
            print(f"{project_id}: page {page}")
            pipelines = get(
                f"https://gitlab.com/api/v4/projects/{project_id}/pipelines?per_page=100&page={page}").json()
            for pipeline in pipelines:
                yield pipeline

            page += 1

    pipelines = filter(lambda x: x["status"] == "success", get_pipelines())
    pipelines = list(itertools.islice(pipelines, pipeline_nums))

    durations = []

    for pipeline in pipelines:
        pipeline_id = pipeline["id"]
        print(f"{project_id}: pipeline ID {pipeline_id}")
        pipeline_detail = get(f"https://gitlab.com/api/v4/projects/{project_id}/pipelines/{pipeline_id}").json()

        duration = pipeline_detail["duration"]
        durations.append(duration)

    return durations


if __name__ == '__main__':
    main()
