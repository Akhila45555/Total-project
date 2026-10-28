import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CONTEXT_DEV_API_KEY")

if not API_KEY:
    raise ValueError("CONTEXT_DEV_API_KEY is missing in .env")

API_URL = "https://api.context.dev/v1/web/extract"

# Job sources
SOURCES = {
    "Naukri": "https://www.naukri.com/jobs-in-india",
    "LinkedIn": "https://www.linkedin.com/jobs/search/?location=India"
}

schema = {
    "type": "object",
    "properties": {
        "jobs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "job_title": {
                        "type": "string",
                        "description": "Job title"
                    },
                    "company": {
                        "type": "string",
                        "description": "Company name"
                    },
                    "location": {
                        "type": "string",
                        "description": "Job location"
                    },
                    "work_mode": {
                        "type": "string",
                        "description": "Remote, Hybrid, or On-site if stated"
                    },
                    "employment_type": {
                        "type": "string",
                        "description": "Full Time, Part Time, Contract, etc. if stated"
                    },
                    "job_url": {
                        "type": "string",
                        "description": "Job application URL"
                    }
                },
                "required": [
                    "job_title",
                    "company",
                    "location",
                    "work_mode",
                    "employment_type",
                    "job_url"
                ]
            }
        }
    },
    "required": ["jobs"]
}

all_jobs = []

for source, url in SOURCES.items():

    print(f"\nScraping {source}...")

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "url": url,
                "schema": schema,
                "maxPages": 1
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        jobs = result.get("data", {}).get("jobs", [])

        for job in jobs:
            job["source"] = source
            all_jobs.append(job)

        print(f"{source}: {len(jobs)} jobs found")

    except Exception as error:
        print(f"{source} error: {error}")


# Save all scraped jobs
with open(
    "day34_job_data.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        all_jobs,
        file,
        indent=4,
        ensure_ascii=False
    )


# Display jobs
print("\n" + "=" * 60)
print("DAY 34 - SCRAPED JOB DATA")
print("=" * 60)

for i, job in enumerate(all_jobs, 1):

    print(f"\nJob {i}")
    print("Job Title       :", job.get("job_title", "N/A"))
    print("Company         :", job.get("company", "N/A"))
    print("Location        :", job.get("location", "N/A"))
    print("Work Mode       :", job.get("work_mode", "N/A"))
    print("Employment Type :", job.get("employment_type", "N/A"))
    print("Source          :", job.get("source", "N/A"))
    print("Job URL         :", job.get("job_url", "N/A"))
    print("-" * 60)

print("\nTotal Jobs:", len(all_jobs))
print("Saved to: day34_job_data.json")