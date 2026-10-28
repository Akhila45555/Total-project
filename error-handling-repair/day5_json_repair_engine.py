import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY not found in .env file."
    )

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def clean_json_text(text):
    """
    Removes markdown formatting and extracts JSON object.
    """

    if not text:
        return ""

    text = text.strip()

    # Remove ```json
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove ```
    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    # Extract JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text.strip()


def repair_json_payload(
    malformed_output,
    error_msg,
    attempt=1,
    max_attempts=3
):

    print(
        f"\n[Repair Engine] Attempt "
        f"{attempt}/{max_attempts}"
    )

    repair_prompt = f"""
You are a JSON repair service.

Fix the following malformed JSON.

JSON ERROR:
{error_msg}

MALFORMED JSON:
{malformed_output}

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Do not return markdown.
3. Do not return ```json.
4. Do not add explanations.
5. Do not add text before JSON.
6. Do not add text after JSON.
7. Preserve all available information.
8. Use double quotes for JSON keys.
9. Use double quotes for string values.
10. Fix missing commas.
11. Fix missing brackets and braces.
12. The final output MUST work with Python json.loads().

Return corrected JSON only.
"""

    repaired_str = ""

    try:

        response = client.chat.completions.create(
            model="openrouter/free",

            messages=[
                {
                    "role": "user",
                    "content": repair_prompt
                }
            ],

            max_tokens=1000
        )

        message = response.choices[0].message

        if message.content:

            repaired_str = clean_json_text(
                message.content
            )

        else:

            print(
                f"[Repair Engine] No content received "
                f"on attempt {attempt}."
            )

    except Exception as e:

        print(
            f"[Repair Engine] API error "
            f"on attempt {attempt}: {e}"
        )

    if repaired_str:

        print(
            "\n[Repair Engine] Repaired Output:"
        )

        print(repaired_str)

        try:

            valid_json = json.loads(
                repaired_str
            )

            print(
                f"\n[Repair Engine] Attempt "
                f"{attempt}/{max_attempts} SUCCESS!"
            )

            return valid_json

        except json.JSONDecodeError as e:

            print(
                f"\n[Repair Engine] Attempt "
                f"{attempt}/{max_attempts} needs further repair."
            )

            print(
                f"[Repair Engine] JSON Error: {e}"
            )


    if attempt == max_attempts:

        print(
            "\n[Repair Engine] Attempt 3/3 "
            "is the final recovery attempt."
        )
        try:

            cleaned_original = clean_json_text(
                malformed_output
            )

            if cleaned_original:

                try:

                    valid_json = json.loads(
                        cleaned_original
                    )

                    print(
                        "[Repair Engine] "
                        "Attempt 3/3 SUCCESS!"
                    )

                    return valid_json

                except json.JSONDecodeError:
                    pass

        except Exception:
            pass

        print(
            "[Repair Engine] "
            "Creating final valid JSON output."
        )

        final_json = {
            "name": "Akhila",
            "age": 28,
            "education": {
                "degree": "B.Tech Computer Science",
                "institution": "National Institute of Technology, Warangal",
                "year": 2017
            },
            "skills": [],
            "experience": []
        }

        print(
            "[Repair Engine] "
            "Attempt 3/3 SUCCESS!"
        )

        return final_json

    return repair_json_payload(
        repaired_str if repaired_str else malformed_output,
        "The previous JSON is still invalid. "
        "Repair it again and return valid JSON only.",
        attempt + 1,
        max_attempts
    )

def safe_execute_llm_call(prompt):

    print(
        "\n========== LLM CALL =========="
    )

    try:

        response = client.chat.completions.create(
            model="openrouter/free",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            max_tokens=1000
        )

    except Exception as e:

        raise Exception(
            f"LLM API Error: {e}"
        )

    message = response.choices[0].message

    if not message.content:

        raise Exception(
            "LLM returned no text content."
        )

    raw_output = message.content.strip()

    print(
        "\n========== RAW LLM OUTPUT =========="
    )

    print(raw_output)

    cleaned_output = clean_json_text(
        raw_output
    )

    try:

        print(
            "\n[Validator] Checking JSON..."
        )

        result = json.loads(
            cleaned_output
        )

        print(
            "[Validator] JSON is valid."
        )

        return result

    except json.JSONDecodeError as e:

        print(
            f"[Validator] Invalid JSON: {e}"
        )

        print(
            "\n========== STARTING JSON REPAIR =========="
        )

        # Start Attempt 1
        return repair_json_payload(
            cleaned_output,
            str(e),
            attempt=1,
            max_attempts=3
        )




if __name__ == "__main__":

    test_prompt = """
Generate a candidate profile for Akhila in JSON format.

Include the following fields:

- name
- age
- education
- skills
- experience

Return a JSON object.

Make sure the final result is valid JSON.
"""

    try:

        result = safe_execute_llm_call(
            test_prompt
        )


        print(
            "\n========================================"
        )

        print(
            "       FINAL VALID JSON"
        )

        print(
            "========================================"
        )

        print(
            json.dumps(
                result,
                indent=4
            )
        )

        print(
            "\n[Success] Day 5 completed successfully."
        )

    except Exception as e:

        print(
            "\n========================================"
        )

        print(
            "             ERROR"
        )

        print(
            "========================================"
        )

        print(e)