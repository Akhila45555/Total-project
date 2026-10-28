import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
# Load environment variables
load_dotenv()

# Claude API Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")

)



# SheetDB API URL
SHEETDB_URL = os.getenv(
    "SHEETDB_URL",
    "https://sheetdb.io/api/v1/YOUR_API_ID")

# Sample Resume
sample_resume = """
Akhila Kethireddy
Email: akhila@example.com
Role: GenAI Systems Engineer
Key Skills: Python, Anthropic API, Pipeline Design, SheetDB Integration
"""

# Function to extract profile
def extract_profile_to_json(resume_text):
    prompt = f"""
Extract profile details into JSON with these keys:

Name, Email, Role, Skills.

Do NOT add explanation.
Return only valid JSON.

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500
    )

    message = response.choices[0].message

    if message.content is None:
        raise Exception("LLM returned no content.")

    raw = message.content.strip()

    print("RAW LLM RESPONSE:")
    print(raw)

    return json.loads(raw)
def push_to_sheetdb(data):
    # Get existing records
    response = requests.get(SHEETDB_URL, timeout=10)
    existing_data = response.json()

    existing_emails = set()

    for row in existing_data:
        email = row.get("Email", "").strip().lower()
        if email:
            existing_emails.add(email)

    email = data.get("Email", "").strip().lower()

    if email in existing_emails:
        print(f"Duplicate Found: {email}")
        print("Skipping insertion.")
        return True

    payload = {
        "data": [data]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(
        SHEETDB_URL,
        json=payload,
        headers=headers,
        timeout=10
    )

    return response.status_code == 201


# Main Program
if __name__ == "__main__":

    print("Step 1 : Extracting Resume...")

    profile = extract_profile_to_json(sample_resume)

    print(profile)

    print("Step 2 : Saving to SheetDB...")

    success = push_to_sheetdb(profile)

    if success:
        print("Data Saved Successfully")
    else:
        print("Failed to Save Data")