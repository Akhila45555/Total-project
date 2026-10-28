# import cv2
# import pyaudio
# import threading
# import queue
# import time



# AUDIO_FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000
# CHUNK = 1024

# VIDEO_QUEUE_SIZE = 30
# AUDIO_QUEUE_SIZE = 50



# video_queue = queue.Queue(maxsize=VIDEO_QUEUE_SIZE)
# audio_queue = queue.Queue(maxsize=AUDIO_QUEUE_SIZE)
# stop_event = threading.Event()




# def video_capture():
#     camera = cv2.VideoCapture(0)

#     if not camera.isOpened():
#         print("Error: Unable to open webcam.")
#         stop_event.set()
#         return

#     print("Video thread started.")

#     while not stop_event.is_set():

#         ret, frame = camera.read()

#         if not ret:
#             print("Warning: Unable to read video frame.")
#             continue

#         # Add frame to queue
#         if not video_queue.full():
#             video_queue.put(frame)
#         else:
#             print("Video queue is full. Dropping old frame.")

#         # Display video
#         cv2.imshow("Proctoring Camera", frame)

#         # Press Q to stop
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             stop_event.set()
#             break

#     camera.release()
#     cv2.destroyAllWindows()

#     print("Video thread stopped.")




# def audio_capture():

#     audio = pyaudio.PyAudio()

#     try:
#         stream = audio.open(
#             format=AUDIO_FORMAT,
#             channels=CHANNELS,
#             rate=RATE,
#             input=True,
#             frames_per_buffer=CHUNK
#         )

#         print("Audio thread started.")

#         while not stop_event.is_set():

#             try:
#                 data = stream.read(
#                     CHUNK,
#                     exception_on_overflow=False
#                 )

#                 if not audio_queue.full():
#                     audio_queue.put(data)
#                 else:
#                     print("Audio queue is full.")

#             except Exception as e:
#                 print("Audio capture error:", e)
#                 break

#         stream.stop_stream()
#         stream.close()

#     finally:
#         audio.terminate()

#     print("Audio thread stopped.")




# def processing():

#     print("Processing thread started.")

#     while not stop_event.is_set():

#         # Process video frame
#         if not video_queue.empty():

#             frame = video_queue.get()

#             # Example processing
#             gray = cv2.cvtColor(
#                 frame,
#                 cv2.COLOR_BGR2GRAY
#             )

#             # Here we can add:
#             # Face detection
#             # Gaze detection
#             # Object detection
#             # Proctoring analysis

#         # Process audio
#         if not audio_queue.empty():

#             audio_data = audio_queue.get()

#             # Here we can add:
#             # Whisper transcription
#             # Noise detection
#             # Voice analysis

#         time.sleep(0.01)

#     print("Processing thread stopped.")



# def main():

#     print("Starting Multi-Threaded Audio/Video Ingestion...")

#     # Create threads
#     video_thread = threading.Thread(
#         target=video_capture,
#         name="VideoThread"
#     )

#     audio_thread = threading.Thread(
#         target=audio_capture,
#         name="AudioThread"
#     )

#     processing_thread = threading.Thread(
#         target=processing,
#         name="ProcessingThread"
#     )

#     # Start threads
#     video_thread.start()
#     audio_thread.start()
#     processing_thread.start()

#     try:

#         while not stop_event.is_set():

#             time.sleep(1)

#     except KeyboardInterrupt:

#         print("\nStopping system...")
#         stop_event.set()

#     # Wait for threads
#     video_thread.join()
#     audio_thread.join()
#     processing_thread.join()

#     print("Multi-threaded system stopped successfully.")



# if __name__ == "__main__":
#     main() 

import cv2
import pyaudio
import wave
import threading
import queue
import time


# ============================================================
# Configuration
# ============================================================

AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

VIDEO_QUEUE_SIZE = 30
AUDIO_QUEUE_SIZE = 50

OUTPUT_VIDEO = "output.mp4"
OUTPUT_AUDIO = "output.wav"


# ============================================================
# Queues and Stop Event
# ============================================================

video_queue = queue.Queue(maxsize=VIDEO_QUEUE_SIZE)
audio_queue = queue.Queue(maxsize=AUDIO_QUEUE_SIZE)

stop_event = threading.Event()


# ============================================================
# Video Capture Thread
# ============================================================

def video_capture():

    print("Video thread started.")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Camera could not be opened.")
        stop_event.set()
        return

    # Get camera resolution
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if width <= 0 or height <= 0:
        width = 640
        height = 480

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0 or fps > 60:
        fps = 20.0

    print(f"Camera resolution: {width}x{height}")
    print(f"Camera FPS: {fps}")

    while not stop_event.is_set():

        ret, frame = cap.read()

        if not ret:
            print("ERROR: Could not read video frame.")
            break

        # Put frame into queue
        try:
            video_queue.put(frame, timeout=0.1)
        except queue.Full:
            # Drop old frame if queue is full
            pass

        # Display live video
        cv2.imshow("Multi-Threaded Camera", frame)

        # Press Q to stop
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            print("Q pressed. Stopping...")
            stop_event.set()
            break

    cap.release()

    print("Video thread stopped.")


# ============================================================
# Audio Capture Thread
# ============================================================

def audio_capture():

    print("Audio thread started.")

    audio = pyaudio.PyAudio()

    try:

        stream = audio.open(
            format=AUDIO_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

    except Exception as e:

        print("ERROR: Could not open microphone.")
        print(e)

        stop_event.set()
        audio.terminate()
        return

    while not stop_event.is_set():

        try:

            data = stream.read(
                CHUNK,
                exception_on_overflow=False
            )

            try:
                audio_queue.put(data, timeout=0.1)
            except queue.Full:
                pass

        except Exception as e:

            print("Audio capture error:", e)
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Audio thread stopped.")


# ============================================================
# Processing Thread
# ============================================================

def processing():

    print("Processing thread started.")

    # --------------------------------------------------------
    # Video Writer
    # --------------------------------------------------------

    video_writer = None

    # --------------------------------------------------------
    # Audio data storage
    # --------------------------------------------------------

    audio_frames = []

    while not stop_event.is_set() or not video_queue.empty() or not audio_queue.empty():

        # ----------------------------------------------------
        # Process Video
        # ----------------------------------------------------

        try:

            frame = video_queue.get(timeout=0.05)

            if video_writer is None:

                height, width = frame.shape[:2]

                fourcc = cv2.VideoWriter_fourcc(
                    *"mp4v"
                )

                video_writer = cv2.VideoWriter(
                    OUTPUT_VIDEO,
                    fourcc,
                    20.0,
                    (width, height)
                )

            video_writer.write(frame)

            video_queue.task_done()

        except queue.Empty:
            pass

        # ----------------------------------------------------
        # Process Audio
        # ----------------------------------------------------

        try:

            audio_data = audio_queue.get(timeout=0.05)

            audio_frames.append(audio_data)

            audio_queue.task_done()

        except queue.Empty:
            pass

    # --------------------------------------------------------
    # Release Video Writer
    # --------------------------------------------------------

    if video_writer is not None:
        video_writer.release()

    # --------------------------------------------------------
    # Save Audio File
    # --------------------------------------------------------

    if audio_frames:

        try:

            audio_file = wave.open(
                OUTPUT_AUDIO,
                "wb"
            )

            audio_file.setnchannels(CHANNELS)
            audio_file.setsampwidth(2)
            audio_file.setframerate(RATE)

            audio_file.writeframes(
                b"".join(audio_frames)
            )

            audio_file.close()

        except Exception as e:

            print("Error saving audio:", e)

    print("Processing thread stopped.")


# ============================================================
# Main Function
# ============================================================

def main():

    print()
    print("==============================================")
    print("Starting Multi-Threaded Audio/Video Ingestion")
    print("==============================================")
    print()

    # Create threads

    video_thread = threading.Thread(
        target=video_capture,
        name="VideoThread"
    )

    audio_thread = threading.Thread(
        target=audio_capture,
        name="AudioThread"
    )

    processing_thread = threading.Thread(
        target=processing,
        name="ProcessingThread"
    )

    # Start threads

    processing_thread.start()
    audio_thread.start()
    video_thread.start()

    try:

        # Wait for video thread
        video_thread.join()

    except KeyboardInterrupt:

        print("Keyboard interrupt received.")
        stop_event.set()

    # Make sure all threads stop

    stop_event.set()

    # Wait for audio and processing threads

    audio_thread.join()
    processing_thread.join()

    # Close OpenCV windows

    cv2.destroyAllWindows()

    print()
    print("==============================================")
    print("All threads stopped.")
    print("==============================================")

    print()
    print("Output files:")

    print(f"Video: {OUTPUT_VIDEO}")
    print(f"Audio: {OUTPUT_AUDIO}")


# ============================================================
# Program Entry Point
# ============================================================

if __name__ == "__main__":
    main()
