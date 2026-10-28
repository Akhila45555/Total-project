# import re


# def validate_meet_link(meet_link):
#     """Validate Google Meet link."""

#     pattern = r"^https://meet\.google\.com/[a-z0-9-]+$"

#     return re.match(pattern, meet_link) is not None


# def connect_bot(meet_link):
#     """Accept and validate the Google Meet link."""

#     if not validate_meet_link(meet_link):
#         return {
#             "status": "error",
#             "message": "Invalid Google Meet link"
#         }

#     return {
#         "status": "ready",
#         "message": "Meet link accepted successfully",
#         "meet_link": meet_link
#     }


# if __name__ == "__main__":

#     meet_link = input("Enter Google Meet link: ")

#     result = connect_bot(meet_link)

#     print("\nBot Result:")
#     print(result)

# 
# from speaking import calculate_metrics, evaluate_speech


# def calculate_meet_score(topic, transcript, duration=60):
#     metrics = calculate_metrics(transcript, duration)

#     evaluation = evaluate_speech(topic, transcript)

#     return {
#         "metrics": metrics,
#         "evaluation": evaluation
#     }


# if __name__ == "__main__":

#     print("=" * 50)
#     print("MEET SPEAKING SCORE")
#     print("=" * 50)

#     topic = input("Enter meeting topic: ")

#     transcript = input("\nEnter meeting transcript: ")

#     result = calculate_meet_score(
#         topic,
#         transcript,
#         duration=180
#     )

#     print("\n===== MEET SCORE =====")

#     print("\nSpeaking Metrics:")
#     print("Word Count:", result["metrics"]["word_count"])
#     print("WPM:", result["metrics"]["wpm"])
#     print("Filler Words:", result["metrics"]["filler_count"])

#     print("\nPerformance Score:")
#     print(result["evaluation"])
import os
import re

from google.apps import meet_v2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from groq import Groq

from speaking import calculate_meet_score


SCOPES = [
    "https://www.googleapis.com/auth/meetings.space.readonly"
]


def authenticate_google():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def get_meeting_code(meet_link):
    match = re.search(
        r"meet\.google\.com/([a-zA-Z0-9-]+)",
        meet_link
    )

    if not match:
        raise ValueError("Invalid Google Meet link")

    return match.group(1)


def get_meeting_transcript(meet_link):
    credentials = authenticate_google()

    client = meet_v2.ConferenceRecordsServiceClient(
        credentials=credentials
    )

    meeting_code = get_meeting_code(meet_link)

    # Find the conference record
    request = meet_v2.ListConferenceRecordsRequest(
        filter=f'space.meeting_code = "{meeting_code}"'
    )

    conferences = list(
        client.list_conference_records(request=request)
    )

    if not conferences:
        raise Exception(
            "No conference record found. "
            "Make sure the meeting has already taken place."
        )

    conference = conferences[0]

    print("Conference found:", conference.name)

    # Find transcript
    transcript_request = meet_v2.ListTranscriptsRequest(
        parent=conference.name
    )

    transcripts = list(
        client.list_transcripts(
            request=transcript_request
        )
    )

    if not transcripts:
        raise Exception(
            "No transcript found. "
            "Make sure transcription was enabled in Google Meet."
        )

    transcript = transcripts[0]

    print("Transcript found:", transcript.name)

    # Get transcript entries
    entries_request = meet_v2.ListTranscriptEntriesRequest(
        parent=transcript.name
    )

    entries = list(
        client.list_transcript_entries(
            request=entries_request
        )
    )

    if not entries:
        raise Exception("Transcript contains no entries.")

    text_parts = []

    for entry in entries:
        text_parts.append(entry.text)

    return "\n".join(text_parts)


def create_meeting_summary(transcript):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing in .env")

    client = Groq(api_key=api_key)

    prompt = f"""
Analyze the following Google Meet transcript.

Transcript:
{transcript}

Provide:

1. Meeting Summary
2. Main Topics Discussed
3. Key Points
4. Participant Performance
5. Strengths
6. Areas for Improvement
7. Final Feedback

Keep the answer clear and professional.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a professional meeting evaluator."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def evaluate_meeting(meet_link, topic):
    transcript = get_meeting_transcript(meet_link)

    print("\n===== MEETING TRANSCRIPT =====")
    print(transcript)

    result = calculate_meet_score(
        topic,
        transcript,
        duration=60
    )

    summary = create_meeting_summary(transcript)

    return {
        "transcript": transcript,
        "summary": summary,
        "evaluation": result["evaluation"],
        "metrics": result["metrics"]
    }


if __name__ == "__main__":

    print("=" * 60)
    print("DAY 21 - GOOGLE MEET SPEAKING EVALUATION")
    print("=" * 60)

    meet_link = input("\nPaste Google Meet link: ")

    topic = input("Enter meeting topic: ")

    try:

        result = evaluate_meeting(
            meet_link,
            topic
        )

        print("\n")
        print("=" * 60)
        print("MEETING SUMMARY")
        print("=" * 60)

        print(result["summary"])

        print("\n")
        print("=" * 60)
        print("MEET SCORE")
        print("=" * 60)

        print(result["evaluation"])

        print("\nSpeaking Metrics:")
        print(result["metrics"])

    except Exception as e:

        print("\nERROR:")
        print(str(e))