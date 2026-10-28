import firebase_admin
import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate("firebase_key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Validation Patterns
PAN_PATTERN = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
DOB_PATTERN_1 = r'^\d{4}-\d{2}-\d{2}$'
DOB_PATTERN_2 = r'^\d{2}-\d{2}-\d{4}$'


def validate_pan(pan):
    return bool(re.match(PAN_PATTERN, pan))


def validate_dob(dob):
    return (
        bool(re.fullmatch(DOB_PATTERN_1, dob))
        or
        bool(re.fullmatch(DOB_PATTERN_2, dob))
    )

def log_validation(candidate_id,
                   source_field,
                   validation_status,
                   error_type,
                   sheetdb_row_id):

    # Store Firestore documents as 01, 02, ..., 10
    doc_id = f"{candidate_id:02d}"

    db.collection("validation_logs").document(doc_id).set({
        "candidate_id": candidate_id,
        "source_field": source_field,
        "validation_status": validation_status,
        "error_type": error_type,
        "sheetdb_row_id": sheetdb_row_id,
        "timestamp": datetime.utcnow()
    })


# Load .env
load_dotenv()

SHEETDB_URL = os.getenv("SHEETDB_URL")

# Sample candidates
candidates = [
    {"candidate_id":1,"name":"KETHIREDDY AKHILA","pan":"OXZPK9934H","dob":"25-11-2003"},
    {"candidate_id":2,"name":"SUDHEER KUMAR GANDIKOTA","pan":"RGKPS5835Q","dob":"17-05-2004"},
    {"candidate_id":3,"name":"MADDIKE KARTHIK REDDY","pan":"EZJPR5614Q","dob":"02-11-2002"},
    {"candidate_id":4,"name":"PACCHIKOLLA RAVI KIRAN","pan":"HFPPR8569G","dob":"26-02-2004"},
    {"candidate_id":5,"name":"TALLAPALLI SIVA PRASAD","pan":"NUOPS4535N","dob":"11-11-2002"},
    
   
]

# Process candidates
for candidate in candidates:

    print("Processing:", candidate["candidate_id"])

    status = "pass"
    error = ""

    if not validate_pan(candidate["pan"]):
        status = "fail"
        error = "INVALID_PAN"

    elif not validate_dob(candidate["dob"]):
        status = "fail"
        error = "INVALID_DOB"

    sheetdb_status = "FAILED"

    try:
        # Check if candidate already exists in SheetDB
        check = requests.get(
            f"{SHEETDB_URL}/search?candidate_id={candidate['candidate_id']}"
        )

        if check.status_code == 200 and check.json():
            print(f"Candidate {candidate['candidate_id']} already exists. Skipping...")
            sheetdb_status = "SKIPPED"

        else:
            response = requests.post(
                SHEETDB_URL,
                json={"data": [candidate]}
            )

            print("Status Code:", response.status_code)
            print("Response:", response.text)

            if response.status_code in [200, 201]:
                sheetdb_status = "SUCCESS"
            else:
                sheetdb_status = "FAILED"

    except Exception as e:
        print("Error:", e)
        sheetdb_status = "FAILED"

    finally:
        log_validation(
            candidate["candidate_id"],
            "SheetDB",
            status,
            error,
            sheetdb_status
        )

print("Completed Successfully")