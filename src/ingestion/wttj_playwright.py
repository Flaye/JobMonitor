import json
import os
import re
import sys
import time
from datetime import datetime

from playwright.sync_api import sync_playwright

from src.config import TECH_KEYWORDS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

SEARCH_URL = "https://www.welcometothejungle.com/fr/jobs?query=Software%20engineer&aroundQuery=Paris%2C%20Paris%2C%20Île-de-France%2C%20France"


def fetch_wttj_jobs(url=SEARCH_URL, max_scrolls=3):
    with sync_playwright() as p:
        brower = p.chromium.launch(headless=True)
        page = brower.new_page()
        page.goto(url)

        jobs = set()
        for i in range(max_scrolls):
            print(f"🔁 Scroll {i+1}")
            page.mouse.wheel(0, 3000)
            time.sleep(2)
        job_list = page.get_by_test_id("search-results-list-item-wrapper").all()
        print(f"📝 Found {len(job_list)} job cards.")

        for job_index, card in enumerate(job_list):
            try:
                title = card.get_by_role("heading").first.text_content()
                company = card.get_by_role("img").first.get_attribute("alt")
                details = card.locator("div[class^='sc-fibHhp']")
                contract = None
                location = None
                category = None
                company_size = None
                if details:
                    for detail_index in range(details.count()):
                        block = details.nth(detail_index)
                        icon = block.locator("i").first
                        span = block.locator("span").first
                        try:
                            icon_name = icon.get_attribute("name")
                            text = span.text_content().strip() if span else None

                            if icon_name == "contract":
                                contract = text
                            elif icon_name == "location":
                                location = text
                            elif icon_name == "tag":
                                category = text
                            elif icon_name == "department":
                                company_size = text
                        except Exception as e:
                            print(
                                f"⚠️ Error processing details for card {detail_index}: {e}"
                            )

                link = card.locator("a").first.get_attribute("href")
                # TODO: Add technology extraction from job page
                job = {
                    "title": title.strip() if title else None,
                    "company": company.strip() if company else None,
                    "link": (
                        f"https://www.welcometothejungle.com{link}" if link else None
                    ),
                    "source": "WTTJ",
                    "details": {
                        "contract": contract.strip() if contract else None,
                        "location": location.strip() if location else None,
                        "category": category.strip() if category else None,
                        "company_size": company_size.strip() if company_size else None,
                    },
                    "fetched_at": datetime.now().isoformat(),
                }
                job.update(extract_technologies(job["link"], brower))

                jobs.add(json.dumps(job, ensure_ascii=False))
                print(f"📄 Job {job_index+1}: {title} at {company}")
            except Exception as e:
                print(f"⚠️ Error on card {job_index}:", e)
        brower.close()
        return [json.loads(job) for job in jobs if jobs]


def extract_technologies(link, browser):
    try:
        details_page = browser.new_page()
        details_page.goto(link)
        time.sleep(0.5)  # Wait for the page to load
        text = details_page.locator("body").text_content()
        found = sorted(
            {
                techno
                for techno in TECH_KEYWORDS
                if re.search(rf"\b{re.escape(techno)}\b", text, re.IGNORECASE)
            }
        )
        job_description = details_page.get_by_test_id(
            "job-section-description"
        ).first.text_content()
        return {
            "technologies": found,
            "job_description": job_description,  # pour debug ou NLP futur (limité ici à 1000 caractères)
        }
    except Exception as e:
        print(f"⚠️ Error opening job details page: {e}")
        return []
    finally:
        details_page.close()
