import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def audit_audio_logprobs_groq(audio_file_path, logprob_threshold=-1.0):
    if not os.path.exists(audio_file_path):
        print(f"Error: File '{audio_file_path}' not found.")
        return None

    with open(audio_file_path, "rb") as audio_file:
        print("[Processing] Analyzing audio segments with Groq Whisper...")
        
        response = client.audio.transcriptions.create(
            file=(audio_file_path, audio_file.read()),
            model="whisper-large-v3",
            response_format="verbose_json"
        )

    print("\n--- Segment Logprob Audit ---")
    anomalies = []

    for segment in response.segments:
        start = segment.get("start", 0.0)
        end = segment.get("end", 0.0)
        text = segment.get("text", "")
        avg_logprob = segment.get("avg_logprob", 0.0)

        print(f"[{start:.1f}s - {end:.1f}s] Logprob: {avg_logprob:.3f} | Text: {text.strip()}")

        if avg_logprob < logprob_threshold:
            anomaly_info = {
                "time_window": f"{start:.1f}s - {end:.1f}s",
                "avg_logprob": avg_logprob,
                "text": text.strip(),
                "reason": "LOW_CONFIDENCE_OR_WHISPER_DETECTED"
            }
            anomalies.append(anomaly_info)
            print(f"  --> ANOMALY DETECTED: {anomaly_info['reason']}")

    print("\n--- Whisper Capture Engine Ready. ---")
    return anomalies

if __name__ == "__main__":
    print("Whisper Anomaly Detection Engine Initialized.")
    audit_audio_logprobs_groq("sample.wav", logprob_threshold=-1.0)