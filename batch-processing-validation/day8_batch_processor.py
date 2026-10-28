import os
import re
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")

)


SHEETDB_URL = os.getenv(
    "SHEETDB_URL",
    "https://sheetdb.io/api/v1/YOUR_API_ID"
    )

batch_resumes = [
    "Akhila Kethireddy | Email: akhila@example.com | Role: Lead Systems Engineer",
    "John Doe | Email: john.doe@tech.io | Role: Backend Architect",
    "Invalid Record without email details or standard role"
]


def validate_record(record):
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not record.get("Name") or len(record.get("Name")) < 2:
        return False

    if not re.match(email_pattern, record.get("Email", "")):
        return False

    return True


def process_batch(resumes):
    valid_batch = []

    for idx, raw_text in enumerate(resumes):

        prompt = f"""
Extract Name, Email and Role as JSON.

Resume:
{raw_text}
"""

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        try:
            message = response.choices[0].message
            if message.content is None:
                raise Exception("LLM returned no content.")
            raw = message.content.strip()
            print("[Batch] Raw LLM Output:")
            print(raw)
            parsed = json.loads(message.content.strip())

            if validate_record(parsed):
                valid_batch.append(parsed)
                print(f"[Batch] Record {idx+1} validated successfully.")
            else:
                print(f"[Batch] Record {idx+1} failed validation.")

        except Exception as e:
            print(f"[Batch] Record {idx+1} parsing error: {e}")

    
    


    try:
        response = requests.get(SHEETDB_URL, timeout=10)
        existing_data = response.json()

        existing_emails = set()
        for row in existing_data:
           email = row.get("Email", "").strip().lower()
           if email:
            existing_emails.add(email)
        

        new_records = []

        for record in valid_batch:
            email = record.get("Email", "").strip().lower()

            if email not in existing_emails:
                new_records.append(record)
                existing_emails.add(email)
            else:
                print(f"Duplicate skipped: {email}")

        if new_records:
            res = requests.post(
                SHEETDB_URL,
                json={"data": new_records},
                timeout=10
            )

            print(f"[Batch Ingestion] Status Code: {res.status_code}")
            print(res.text)
        else:
            print("No new records to insert.")

    except Exception as e:
        print(f"SheetDB Error: {e}")


if __name__ == "__main__":
    process_batch(batch_resumes)