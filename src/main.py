import os
from datetime import datetime
from multiprocessing.pool import RUN

from src.ingestion.wttj_playwright import fetch_wttj_jobs
from src.processing.clean_jobs import clean_jobs, load_raw_jobs, save_cleaned_jobs
from src.utils import save_jobs

RUN_SCRAPPING = True
RUN_CLEANING = True

if __name__ == "__main__":
    if not os.path.exists("data/raw/"):
        os.makedirs("data/raw/")
    if not os.path.exists("data/processed/"):
        os.makedirs("data/processed/")

    if RUN_SCRAPPING:
        print("🔍 Starting job fetching...")
        start_time = datetime.now()
        jobs = fetch_wttj_jobs()
        save_jobs(jobs, "data/raw/wttj_jobs_playwright.json")
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"⏱️  Duration: {duration}")
        print("✅ Job fetching completed.")

    if RUN_CLEANING:
        print("🧹 Starting job cleaning...")
        jobs = load_raw_jobs("wttj_jobs_playwright.json")
        if not jobs:
            print("⚠️ No jobs found to clean.")
            exit(1)
        cleaned_jobs = clean_jobs(jobs)
        save_cleaned_jobs(cleaned_jobs, "wttj_cleaned_jobs.csv")
