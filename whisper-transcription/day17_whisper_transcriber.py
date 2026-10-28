# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# def transcribe_audio_sample(audio_file_path):

#     if not os.path.exists(audio_file_path):
#         print(f"Error: File '{audio_file_path}' not found.")
#         return None

#     with open(audio_file_path, "rb") as audio_file:

#         print("[Processing] Sending audio stream to Whisper API...")

#         transcription = client.audio.transcriptions.create(
#             model="whisper-1",
#             file=audio_file,
#             response_format="verbose_json"
#         )

#     print("\n--- Transcription Text ---")
#     print(transcription.text)

#     return transcription


# if __name__ == "__main__":

#     print("Whisper Transcription Module Initialized.")

#     audio_file = "sample.wav"

#     transcribe_audio_sample(audio_file)

# import os
# import base64
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("OPENROUTER_API_KEY")


# def transcribe_audio_sample(audio_file_path):

#     if not os.path.exists(audio_file_path):
#         print(f"Error: File '{audio_file_path}' not found.")
#         return None

#     with open(audio_file_path, "rb") as audio_file:
#         audio_data = base64.b64encode(audio_file.read()).decode("utf-8")

#     print("[Processing] Sending audio to OpenRouter...")

#     response = requests.post(
#         "https://openrouter.ai/api/v1/audio/transcriptions",
#         headers={
#             "Authorization": f"Bearer {API_KEY}",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model": "openai/whisper-1",
#             "input_audio": {
#                 "data": audio_data,
#                 "format": "wav"
#             }
#         }
#     )

#     if response.status_code != 200:
#         print("Error:", response.status_code)
#         print(response.text)
#         return None

#     result = response.json()

#     print("\n--- Transcription Text ---")
#     print(result["text"])

#     return result


# if __name__ == "__main__":

#     print("OpenRouter Transcription Module Initialized.")

#     transcribe_audio_sample("sample.wav")

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio_free(audio_file_path):
    if not os.path.exists(audio_file_path):
        print(f"Error: File '{audio_file_path}' not found.")
        return None

    with open(audio_file_path, "rb") as audio_file:
        print("[Processing] Sending audio stream to Groq Whisper API...")
        transcription = client.audio.transcriptions.create(
            file=(audio_file_path, audio_file.read()),
            model="whisper-large-v3",
            response_format="verbose_json"
        )

    print("\n--- Transcription Text ---")
    print(transcription.text)
    return transcription

if __name__ == "__main__":
    transcribe_audio_free("sample.wav")