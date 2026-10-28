import requests
import json

BASE_URL = "http://127.0.0.1:5600/api/0"


def list_buckets():
    url = f"{BASE_URL}/buckets"
    response = requests.get(url)

    print("\n===== BUCKETS =====")
    print(json.dumps(response.json(), indent=4))


def window_events():
    bucket = "aw-watcher-window_DESKTOP-JLPD3EM"
    url = f"{BASE_URL}/buckets/{bucket}/events"

    response = requests.get(url)

    print("\n===== WINDOW EVENTS =====")
    events = response.json()

    for event in events[:10]:
        print(f"Timestamp : {event.get('timestamp')}")
        print(f"Duration  : {event.get('duration')}")

        data = event.get("data", {})
        print(f"App        : {data.get('app')}")
        print(f"Title      : {data.get('title')}")
        print("-" * 50)


def afk_events():
    bucket = "aw-watcher-afk_DESKTOP-JLPD3EM"
    url = f"{BASE_URL}/buckets/{bucket}/events"

    response = requests.get(url)

    print("\n===== AFK EVENTS =====")
    events = response.json()

    for event in events[:10]:
        print(f"Timestamp : {event.get('timestamp')}")
        print(f"Duration  : {event.get('duration')}")
        print(f"Status    : {event.get('data')}")
        print("-" * 50)


if __name__ == "__main__":
    list_buckets()
    window_events()
    afk_events()