import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision




base_options = python.BaseOptions(
    model_asset_path="face_landmarker.task"
)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
    num_faces=1
)

detector = vision.FaceLandmarker.create_from_options(options)



cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

print("=" * 50)
print("DAY 23 - FACIAL LANDMARK & GAZE TRACKING")
print("=" * 50)
print("Webcam started.")
print("Look Left / Center / Right")
print("Press 'q' to stop.")




while True:

    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame")
        break

    
    frame = cv2.resize(frame, (640, 480))

    
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # Detect face landmarks
    result = detector.detect(mp_image)


    

    if result.face_landmarks:

        face_landmarks = result.face_landmarks[0]
    
        height, width, _ = frame.shape


        

        for landmark in face_landmarks:

            x = int(landmark.x * width)
            y = int(landmark.y * height)

            cv2.circle(
                frame,
                (x, y),
                1,
                (255, 255, 255),
                -1
            )


        

        left_eye_outer = face_landmarks[33]
        left_eye_inner = face_landmarks[133]

        right_eye_inner = face_landmarks[362]
        right_eye_outer = face_landmarks[263]




        left_iris = face_landmarks[468]
        right_iris = face_landmarks[473]


        
        left_iris_x = int(left_iris.x * width)
        left_iris_y = int(left_iris.y * height)

        right_iris_x = int(right_iris.x * width)
        right_iris_y = int(right_iris.y * height)


       

        cv2.circle(
            frame,
            (left_iris_x, left_iris_y),
            5,
            (255, 255, 255),
            -1
        )

        cv2.circle(
            frame,
            (right_iris_x, right_iris_y),
            5,
            (255, 255, 255),
            -1
        )


        

        left_denominator = (
            left_eye_inner.x - left_eye_outer.x
        )

        right_denominator = (
            right_eye_outer.x - right_eye_inner.x
        )


        # Avoid division by zero

        if (
            abs(left_denominator) < 0.0001
            or abs(right_denominator) < 0.0001
        ):
            gaze = "Unknown"

        else:

            left_ratio = (
                left_iris.x - left_eye_outer.x
            ) / left_denominator

            right_ratio = (
                right_iris.x - right_eye_inner.x
            ) / right_denominator


            # Average both eyes

            gaze_ratio = (
                left_ratio + right_ratio
            ) / 2


        

            if gaze_ratio < 0.40:

                gaze = "Looking Left"

            elif gaze_ratio > 0.60:

                gaze = "Looking Right"

            else:

                gaze = "Looking Center"


        

        cv2.putText(
            frame,
            "Gaze: " + gaze,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )


   
    else:

        cv2.putText(
            frame,
            "Face not detected",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )


    

    cv2.imshow(
        "Day 23 - Facial Landmark & Gaze Tracking",
        frame
    )


    

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break



cap.release()

detector.close()

cv2.destroyAllWindows()

print("Gaze tracking stopped.")