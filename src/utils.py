import json


def save_jobs(jobs, filename="data/raw/default_filename.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
