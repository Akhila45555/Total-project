import cv2
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import time

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

print("Firebase connected successfully")



face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)



def send_alert(alert_type, severity, message):

    data = {
        "candidate_id": "CAND_001",
        "alert_type": alert_type,
        "severity": severity,
        "source": "OpenCV",
        "message": message,
        "timestamp": datetime.now(timezone.utc)
    }

    db.collection("telemetry_logs").add(data)

    print("\n==============================")
    print("ALERT SENT TO FIREBASE")
    print("Alert    :", alert_type)
    print("Severity :", severity)
    print("Message  :", message)
    print("==============================")


# ---------------- CAMERA ----------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened")
    exit()

print("Camera started")
print("Press Q to stop")

last_alert = ""
last_time = 0

while True:

    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read camera")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    face_count = len(faces)

    # Draw face boxes
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    # ---------------- DETECTION ----------------

    if face_count == 0:

        status = "ALERT"
        message = "Face Missing"
        alert_type = "face_missing"
        severity = "HIGH"

    elif face_count > 1:

        status = "ALERT"
        message = "Multiple Faces Detected"
        alert_type = "multiple_faces"
        severity = "HIGH"

    else:

        status = "NORMAL"
        message = "Face Detected"
        alert_type = "normal"
        severity = "LOW"


    # ---------------- DISPLAY ----------------

    cv2.putText(
        frame,
        f"Faces Detected: {face_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Status: {status}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0) if status == "NORMAL" else (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        message,
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0) if status == "NORMAL" else (0, 0, 255),
        2
    )


    # ---------------- FIREBASE ALERT ----------------

    current_time = time.time()

    if (
        status == "ALERT"
        and
        (
            alert_type != last_alert
            or current_time - last_time >= 3
        )
    ):

        send_alert(
            alert_type,
            severity,
            message
        )

        last_alert = alert_type
        last_time = current_time


    # ---------------- SHOW CAMERA ----------------

    cv2.imshow(
        "Day 27 - Firebase Telemetry Proctoring",
        frame
    )


    # Press Q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()

print("Day 27 completed")