# import os
# import requests
# from dotenv import load_dotenv

# # Load .env file
# load_dotenv()

# # Read API URL
# SHEETDB_API_URL = os.getenv("SHEETDB_API_URL")

# def append_candidate_record(name, email, role, status="Verified"):
#     print(f"[SheetDB Ingestion] Preparing row payload for: {name}")

#     payload = {
#         "data": [
#             {
#                 "Name": name,
#                 "Email": email,
#                 "Role": role,
#                 "Status": status
#             }
#         ]
#     }

#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json"
#     }

#     try:
#         response = requests.post(
#             SHEETDB_API_URL,
#             json=payload,
#             headers=headers,
#             timeout=10
#         )

#         print(f"[SheetDB Ingestion] HTTP Status Code: {response.status_code}")

#         if response.status_code == 201:
#             print("[SheetDB Ingestion] Record appended successfully!")
#             print(response.json())
#         else:
#             print("[SheetDB Failure]")
#             print(response.text)

#     except Exception as e:
#         print("[SheetDB Exception]")
#         print(e)


# if __name__ == "__main__":
#     append_candidate_record(
#         name="Akhila Kethireddy",
#         email="akhila@example.com",
#         role="GenAI Systems Engineer"
#     )

import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read SheetDB API URL
SHEETDB_URL = os.getenv(
    "SHEETDB_URL",
    "https://sheetdb.io/api/v1/YOUR_API_ID"
)

def append_candidate_record(name, email, role, status="Verified"):

    print(f"[SheetDB Ingestion] Preparing row payload for: {name}")

    try:
        # Step 1: Get existing records
        response = requests.get(SHEETDB_URL, timeout=10)

        if response.status_code == 200:
            existing_data = response.json()

            # Step 2: Check duplicate email
            for row in existing_data:
                if row.get("Email", "").strip().lower() == email.strip().lower():
                    print("Duplicate record found.")
                    print("Skipping insertion.")
                    return

        # Step 3: Create payload
        payload = {
            "data": [
                {
                    "Name": name,
                    "Email": email,
                    "Role": role,
                    "Status": status
                }
            ]
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Step 4: Insert into SheetDB
        response = requests.post(
            SHEETDB_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        print(f"HTTP Status Code: {response.status_code}")

        if response.status_code == 201:
            print("Record inserted successfully")
            print(response.json())
        else:
            print("Failed to insert record")
            print(response.text)
    except Exception as e:
        print("[SheetDB Exception]")
        print(e)


if __name__ == "__main__":
    append_candidate_record(
        name="Akhila Kethireddy",
        email="akhila@example.com",
        role="GenAI Systems Engineer"
    )