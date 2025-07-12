from datetime import datetime

from src.ingestion.wttj_playwright import fetch_wttj_jobs, save_jobs

if __name__ == "__main__":
    start_time = datetime.now()
    jobs = fetch_wttj_jobs()
    save_jobs(jobs, "data/raw/wttj_jobs_playwright.json")
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"⏱️  Duration: {duration}")
