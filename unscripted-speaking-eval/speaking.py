import os
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not found in .env")

client = Groq(api_key=api_key)


def record_audio(duration=10):
    sample_rate = 16000
    channels = 1

    print(f"Start speaking for {duration} seconds...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=channels,
        dtype="int16"
    )

    sd.wait()

    audio_file = "speaking.wav"
    write(audio_file, sample_rate, audio)

    return audio_file


def transcribe_audio(audio_file):

    with open(audio_file, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3-turbo",
            response_format="text",
            language="en",
            temperature=0
        )

    return transcription


def calculate_metrics(recognized_text, duration=10):

    words = recognized_text.split()
    word_count = len(words)

    minutes = duration / 60
    words_per_minute = word_count / minutes

    filler_words = [
        "um",
        "uh",
        "hmm",
        "like",
        "you know",
        "actually",
        "basically"
    ]

    lower_text = recognized_text.lower()

    filler_count = 0

    for filler in filler_words:
        filler_count += lower_text.count(filler)

    return {
        "word_count": word_count,
        "wpm": round(words_per_minute, 2),
        "filler_count": filler_count
    }


def evaluate_speech(topic, recognized_text):

    prompt = f"""
You are an English speaking evaluation assistant.

Topic:
{topic}

Candidate's spoken response:
{recognized_text}

Evaluate the candidate based on:

1. Topic Relevance
2. Clarity
3. Grammar
4. Vocabulary
5. Fluency
6. Overall Performance

Give scores from 0 to 100.

Use this format:

Topic Relevance: XX/100
Clarity: XX/100
Grammar: XX/100
Vocabulary: XX/100
Fluency: XX/100
Overall Score: XX/100

Then provide:

Strengths:
- point 1
- point 2

Areas for Improvement:
- point 1
- point 2

Final Feedback:
Short feedback about the candidate's speaking performance.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a professional English speaking evaluator."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def run_evaluation(topic, duration=10):

    audio_file = record_audio(duration)

    recognized_text = transcribe_audio(audio_file)

    metrics = calculate_metrics(
        recognized_text,
        duration
    )

    evaluation = evaluate_speech(
        topic,
        recognized_text
    )

    return {
        "topic": topic,
        "transcript": recognized_text,
        "metrics": metrics,
        "evaluation": evaluation
    }


# Run from terminal
if __name__ == "__main__":

    topic = "What is Generative AI?"

    print("=" * 50)
    print("DAY 21 - UNSCRIPTED SPEAKING EVALUATION")
    print("=" * 50)

    result = run_evaluation(topic, 10)

    print("\nRecognized Speech:")
    print(result["transcript"])

    print("\nSpeaking Metrics:")
    print(result["metrics"])

    print("\nAssessment:")
    print(result["evaluation"])