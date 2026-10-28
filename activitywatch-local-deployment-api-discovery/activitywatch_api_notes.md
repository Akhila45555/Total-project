# ActivityWatch API Notes

## Objective
Explore the local ActivityWatch REST API and understand the available buckets and event schema.

## Base URL

http://127.0.0.1:5600/api/0

---

## Buckets

GET /buckets

Returned buckets:

- aw-watcher-window_DESKTOP-JLPD3EM
- aw-watcher-afk_DESKTOP-JLPD3EM

### Window Bucket

Purpose:
Stores information about the currently active application and window title.

Example fields:

- timestamp
- duration
- data.app
- data.title

Example:

{
  "timestamp": "2026-08-06T...",
  "duration": 2.0,
  "data": {
    "app": "Microsoft Edge",
    "title": "ActivityWatch"
  }
}

---

### AFK Bucket

Purpose:

Tracks whether the user is Away From Keyboard (AFK).

Later this bucket is used to remove idle time from productivity and focus calculations.

---

## API Calls

### List Buckets

GET

http://127.0.0.1:5600/api/0/buckets

curl

curl http://127.0.0.1:5600/api/0/buckets

---

### Get Window Events

GET

http://127.0.0.1:5600/api/0/buckets/aw-watcher-window_DESKTOP-JLPD3EM/events

curl

curl http://127.0.0.1:5600/api/0/buckets/aw-watcher-window_DESKTOP-JLPD3EM/events

---

### Get AFK Events

GET

http://127.0.0.1:5600/api/0/buckets/aw-watcher-afk_DESKTOP-JLPD3EM/events

curl

curl http://127.0.0.1:5600/api/0/buckets/aw-watcher-afk_DESKTOP-JLPD3EM/events

---

### Query by Time Range

GET

/api/0/buckets/<bucket_name>/events?start=<ISO_TIME>&end=<ISO_TIME>

Example

http://127.0.0.1:5600/api/0/buckets/aw-watcher-window_DESKTOP-JLPD3EM/events?start=2026-08-06T00:00:00Z&end=2026-08-06T23:59:59Z