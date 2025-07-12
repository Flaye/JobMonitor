import json
import os
import re
from datetime import datetime

import pandas as pd

RAW_PATH = "data/raw/"
OUT_PATH = "data/processed/"


def load_raw_jobs(filename):
    """
    Load raw jobs from a JSON file.
    """
    filepath = os.path.join(RAW_PATH, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} does not exist.")

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def clean_jobs(jobs):
    records = []
    for job in jobs:
        record = {
            "title": job.get("title").strip() if job.get("title") else None,
            "company": job.get("company").strip() if job.get("company") else None,
            "link": job.get("link"),
            "source": job.get("source"),
            "fetched_at": job.get("fetched_at"),
            "contract": job.get("details", {}).get("contract"),
            "location": job.get("details", {}).get("location"),
            "category": job.get("details", {}).get("category"),
            "nb_colaboarateurs": (
                re.search(
                    r"([A-Za-z0-9]* ?[A-Za-z0-9]*) collaborateurs",
                    job.get("details", {}).get("company_size"),
                ).group(1)
                if job.get("details", {}).get("company_size")
                else None
            ),
            "technologies": eval(job.get("technologies", [])),
            "is_remote": "remote" in job.get("location", "").lower()
            or job.get("title", "").lower()
            in ["remote", "work from home", "télétravail"],
            "description": job.get("job_description", ""),
        }
        records.append(record)
    return pd.DataFrame(records)


def save_cleaned_jobs(df, filename):
    """
    Save cleaned jobs to a CSV file.
    """
    filepath = os.path.join(OUT_PATH, filename)
    df.to_csv(filepath, index=False, encoding="utf-8")
    print(f"✅ Cleaned jobs saved to {filepath}")
