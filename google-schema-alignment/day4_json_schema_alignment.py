import os
import json
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

# Initialize Claude client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    

      api_key=os.getenv("OPENROUTER_API_KEY"),
        

     )
# Candidate profile
candidate_profile_context = (
    "Name: Akhila Kethireddy, "
    "Email: akhila@example.com, "
    "Core Skill: GenAI Infrastructure"
)

# System Prompt
json_alignment_instruction = """
You are an enterprise schema mapping middleware component.
Convert the provided candidate details directly into a minified JSON object matching
the strict Google Schema specifications.

Required JSON Structure:
{
    "@context": "https://schema.org"
    "@type": "Person"
    "name": ""
    "email": ""
    "jobTitle": ""
}

CRITICAL RULES:
1. Respond with a valid, clean, single-line minified JSON string ONLY.
2. Do NOT wrap the JSON inside markdown code blocks.
3. No comments, whitespace formatting, or conversational notes are allowed.
"""

def compile_google_schema_payload(context_data):
    try:
        messages = [
            {
                "role": "system",
                "content": json_alignment_instruction
            },
            {
                "role": "user",
                "content": f"Target Data Matrix: {context_data}"
            }
        ]

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            max_tokens=500
        )

        raw_json_string = response.choices[0].message.content.strip()

        # Verify JSON format
        json.loads(raw_json_string)

        return raw_json_string

    except json.JSONDecodeError:
        return (
            "Error: Output failed to maintain strict, "
            "un-wrapped minified JSON formatting rules."
        )

    except Exception as e:
        return f"Execution Pipeline Failure: {str(e)}"


if __name__ == "__main__":
    print("--- Executing Day 4 Google Schema JSON Compilation Engine ---")

    schema_compliant_json = compile_google_schema_payload(
        candidate_profile_context
    )

    print(schema_compliant_json)