import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Model name directly in Python code
MODEL = "openrouter/free"

if not API_KEY:
    raise ValueError("Please add OPENROUTER_API_KEY to your .env file")

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


# Evaluation result format
class CandidateEvaluation(BaseModel):
    candidate_name: str
    matching_score: int = Field(ge=0, le=100)
    matched_skills: list[str]
    missing_skills: list[str]
    experience_comparison: str
    recommendation: str
    evaluation_summary: str


# Java Developer job description
JOB_DESCRIPTION = """
Job Title: Java Developer

Required Skills:
- Java programming
- Spring Boot
- Hibernate
- SQL
- REST API development
- 2 years of Java development experience
"""

# Sample resume for Akhila
SAMPLE_RESUME = """
Name: Akhila
Experience: 2 years

Skills:
- Python
- SQL
- REST APIs
- Git

"""


def evaluate_candidate(job_description, resume):
    prompt = f"""
You are a fair, evidence-based recruitment assistant.

Compare the candidate resume with the job description.

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume}

Evaluation rules:
1. Score job-related skills and experience from 0 to 100.
2. Check Java, Spring Boot, Hibernate, SQL and REST APIs.
3. Do not assume a skill exists if the resume does not mention it.
4. Missing evidence does not prove the candidate lacks the skill.
5. Give a recommendation:
   - "Potential Match" if the score is 70 or higher.
   - "Not a Match" if the score is below 70.
6. Use only job-related evidence.
7. Do not invent candidate details.
8. Return ONLY valid JSON with these keys:
candidate_name, matching_score, matched_skills, missing_skills,
experience_comparison, recommendation, evaluation_summary.

Return the score according to the actual resume evidence.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Evaluate candidates using job-related evidence only."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("AI returned an empty response")

    content = content.strip()

    # Handle optional Markdown code fences
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content[:-3].strip()
        if content.lower().startswith("json"):
            content = content[4:].strip()

    data = json.loads(content)
    result = CandidateEvaluation.model_validate(data)

    # Apply the rejection threshold consistently in Python
    result.recommendation = (
        "Potential Match"
        if result.matching_score >= 70
        else "Not a Match"
    )

    return result


def main():
    print("=" * 50)
    print("DAY 36 - CANDIDATE EVALUATION AGENT")
    print("AI Provider: OpenRouter")
    print("=" * 50)

    print("\nJOB DESCRIPTION:")
    print(JOB_DESCRIPTION)

    print("\nCANDIDATE RESUME:")
    print(SAMPLE_RESUME)

    try:
        result = evaluate_candidate(
            JOB_DESCRIPTION,
            SAMPLE_RESUME
        )

        print("\n--- EVALUATION REPORT ---")
        print(result.model_dump_json(indent=2))

        print("\n--- FINAL RESULT ---")
        if result.recommendation == "Not a Match":
            print("REJECTED / NOT A MATCH")
        else:
            print("POTENTIAL MATCH")

    except Exception as error:
        print("\nEvaluation failed:", str(error))
        print("Check your API key, model availability and connection.")


if __name__ == "__main__":
    main()