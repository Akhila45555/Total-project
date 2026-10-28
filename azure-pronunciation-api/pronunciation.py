import os
import difflib
import sounddevice as sd
import wave

from groq import Groq
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -------------------------------
# Configuration
# -------------------------------

SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 10

AUDIO_FILE = "pronunciation.wav"
REFERENCE_TEXT = (
      "Artificial intelligence helps computers "
      "understand human speech."
)


# -------------------------------
# Record user's speech
# -------------------------------

print("===================================")
print("   PRONUNCIATION ASSESSMENT")
print("===================================")

print("\nReference sentence:")
print(REFERENCE_TEXT)

print("\nGet ready...")
print("Speak the sentence after recording starts.")

recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16"
)

sd.wait()

print("\nRecording completed.")


# -------------------------------
# Save audio
# -------------------------------

with wave.open(AUDIO_FILE, "wb") as audio:

    audio.setnchannels(CHANNELS)
    audio.setsampwidth(2)
    audio.setframerate(SAMPLE_RATE)

    audio.writeframes(recording.tobytes())

print("Audio saved successfully.")


# -------------------------------
# Speech to Text using Groq
# -------------------------------

print("\nConverting speech to text...")

with open(AUDIO_FILE, "rb") as audio_file:

    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3-turbo",
        language="en",
        response_format="text"
    )


recognized_text = transcription.strip()


print("\nRecognized Text:")
print(recognized_text)


# -------------------------------
# Reference Matching
# -------------------------------
reference = REFERENCE_TEXT.lower().split()
recognized = recognized_text.lower().split()

matcher = difflib.SequenceMatcher(
    None,
    reference,
    recognized
)

match_score = matcher.ratio() * 100


# -------------------------------
# Display Assessment
# -------------------------------

print("\n===================================")
print("       ASSESSMENT RESULT")
print("===================================")

print(f"\nReference Match Score: {match_score:.2f}%")

if match_score >= 90:

    print("Assessment: Excellent")

elif match_score >= 75:

    print("Assessment: Good")

elif match_score >= 50:

    print("Assessment: Needs Improvement")

else:

    print("Assessment: Poor")


# -------------------------------
# Word Comparison
# -------------------------------

print("\nWord Comparison:")
for word in reference:

    if word in recognized:

        print(f"✓ {word}")

    else:

        print(f"✗ {word} - Missing")


print("\nAssessment completed successfully.")