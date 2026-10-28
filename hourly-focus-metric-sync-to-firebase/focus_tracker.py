import requests
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import json
import time


BASE_URL = "http://127.0.0.1:5600/api/0"



DEV_APPS = [
    "Code.exe",
    "WindowsTerminal.exe",
    "cmd.exe",
    "powershell.exe",
    "Postman.exe",
    "pycharm64.exe",
    "chrome.exe",
    "msedge.exe"
]



cred = credentials.Certificate("serviceAccountKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()



def get_buckets():

    response = requests.get(
        f"{BASE_URL}/buckets"
    )

    response.raise_for_status()

    return response.json()


def find_bucket(bucket_type):

    buckets = get_buckets()

    for bucket_id in buckets.keys():

        if bucket_type in bucket_id:
            return bucket_id

    return None


def get_events(bucket_id):

    if not bucket_id:
        return []

    start = (
        datetime.utcnow() - timedelta(days=1)
    ).isoformat() + "Z"

    end = (
        datetime.utcnow()
    ).isoformat() + "Z"

    url = (
        f"{BASE_URL}/buckets/"
        f"{bucket_id}/events"
    )

    params = {
        "start": start,
        "end": end
    }

    response = requests.get(
        url,
        params=params
    )

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# Convert Seconds to Hours and Minutes
# --------------------------------------------------

def format_time(seconds):

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    return hours, minutes


# --------------------------------------------------
# Upload Focus Data to Firebase
# --------------------------------------------------

def upload_to_firebase(app, minutes):

    data = {

        "date": datetime.now().strftime(
            "%Y-%m-%d"
        ),

        "hour": datetime.now().strftime(
            "%H"
        ),

        "app": app,

        "duration_minutes": minutes
    }

    retries = 3
    delay = 1

    while retries > 0:

        try:

            db.collection(
                "dev_focus_metrics"
            ).add(data)

            print(
                f"{app} uploaded successfully"
            )

            return

        except Exception as e:

            print(
                "Upload Failed:",
                e
            )

            retries -= 1

            time.sleep(delay)

            delay *= 2

    # Save failed data locally

    with open(
        "failed_focus_data.json",
        "a"
    ) as file:

        file.write(
            json.dumps(data) + "\n"
        )


# --------------------------------------------------
# Main Processing
# --------------------------------------------------

window_bucket = find_bucket(
    "window"
)

afk_bucket = find_bucket(
    "afk"
)


# Check buckets

if not window_bucket:

    print(
        "Window bucket not found."
    )

    exit()

if not afk_bucket:

    print(
        "AFK bucket not found."
    )

    exit()


# Get events

window_events = get_events(
    window_bucket
)

afk_events = get_events(
    afk_bucket
)


# --------------------------------------------------
# Developer Focus Summary
# --------------------------------------------------

print("=" * 50)

print(
    "Developer Focus Summary"
)

print("=" * 50)


focus_time = {}


# Calculate focus time

for event in window_events:

    app = event.get(
        "data",
        {}
    ).get(
        "app",
        ""
    )

    duration = event.get(
        "duration",
        0
    )

    if app in DEV_APPS:

        if app not in focus_time:

            focus_time[app] = 0

        focus_time[app] += duration


# --------------------------------------------------
# Display Focus Time in Hours
# --------------------------------------------------

total_seconds = 0


for app, seconds in focus_time.items():

    hours, minutes = format_time(
        seconds
    )

    total_seconds += seconds

    print(
        f"{app:25} "
        f"{hours} hours "
        f"{minutes} minutes"
    )

    # Firebase still stores minutes

    upload_to_firebase(
        app,
        round(seconds / 60, 2)
    )


# --------------------------------------------------
# Total Focus Time
# --------------------------------------------------

total_hours, total_minutes = format_time(
    total_seconds
)


print("-" * 50)

print(
    f"Total Focus Time : "
    f"{total_hours} hours "
    f"{total_minutes} minutes"
)


# --------------------------------------------------
# Calculate Idle Time
# --------------------------------------------------

idle = 0


for event in afk_events:

    status = event.get(
        "data",
        {}
    ).get(
        "status",
        ""
    )

    if status == "afk":

        idle += event.get(
            "duration",
            0
        )


# --------------------------------------------------
# Display Idle Time in Hours
# --------------------------------------------------

idle_hours, idle_minutes = format_time(
    idle
)


print(
    f"Idle Time        : "
    f"{idle_hours} hours "
    f"{idle_minutes} minutes"
)

print("=" * 50)

print(
    "Focus tracker completed successfully."
)