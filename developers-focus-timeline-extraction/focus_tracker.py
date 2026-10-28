import requests
from datetime import datetime, timedelta



BASE_URL = "http://127.0.0.1:5600/api/0"

# Developer applications
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


def get_buckets():
    response = requests.get(f"{BASE_URL}/buckets")
    return response.json()


def find_bucket(bucket_type):
    buckets = get_buckets()

    for bucket_id in buckets.keys():
        if bucket_type in bucket_id:
            return bucket_id

    return None


def get_events(bucket_id):
    start = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"
    end = datetime.utcnow().isoformat() + "Z"

    url = f"{BASE_URL}/buckets/{bucket_id}/events"

    params = {
        "start": start,
        "end": end
    }

    response = requests.get(url, params=params)
    return response.json()


window_bucket = find_bucket("window")
afk_bucket = find_bucket("afk")

window_events = get_events(window_bucket)
afk_events = get_events(afk_bucket)

print("=" * 50)
print("Developer Focus Summary")
print("=" * 50)

focus_time = {}

for event in window_events:

    app = event["data"].get("app", "")
    duration = event.get("duration", 0)

    if app in DEV_APPS:

        if app not in focus_time:
            focus_time[app] = 0

        focus_time[app] += duration

total = 0

for app, seconds in focus_time.items():
    minutes = round(seconds / 60, 2)
    total += minutes
    print(f"{app:25} {minutes} minutes")

print("-" * 50)
print(f"Total Focus Time : {round(total,2)} minutes")

idle = 0

for event in afk_events:

    status = event["data"].get("status", "")

    if status == "afk":
        idle += event["duration"]

print(f"Idle Time        : {round(idle/60,2)} minutes")