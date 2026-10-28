# import os
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# def transcribe_audio_groq(audio_file_path: str):
#     # Initialize Groq client with API key
#     client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#     if not os.path.exists(audio_file_path):
#         print(f"Error: Audio file '{audio_file_path}' not found.")
#         return

#     print(f"Transcribing {audio_file_path} using Groq Whisper...")
    
#     with open(audio_file_path, "rb") as audio_file:
#         transcription = client.audio.transcriptions.create(
#             file=(audio_file_path, audio_file.read()),
#             model="whisper-large-v3-turbo",  # Fast Speech-to-Text model
#             response_format="text"
#         )
        
#     print("\n✅ Recognized Text:")
#     print(transcription)

# if __name__ == "__main__":
#     # Test with your sample audio file
#     transcribe_audio_groq("sample.wav")

import os
import sounddevice as sd
from scipy.io.wavfile import write
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing in .env file")

# Create Groq client
client = Groq(api_key=api_key)

# Audio settings
sample_rate = 16000
duration = 5

print("=================================")
print("     Groq Speech-to-Text - Day 19")
print("=================================")

print(f"Recording for {duration} seconds...")
print("Please speak now...")

# Record audio from microphone
audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

# Save recording
audio_file = "recording.wav"
write(audio_file, sample_rate, audio)

print("Recording completed.")
print("Sending audio to Groq...")

# Send audio to Groq Whisper modelgit 
with open(audio_file, "rb") as file:

    transcription = client.audio.transcriptions.create(
        file=(audio_file, file.read()),
        model="whisper-large-v3-turbo",
        response_format="text"
    )

print("\nSpeech recognized successfully!")
print("Recognized Text:")
print(transcription)