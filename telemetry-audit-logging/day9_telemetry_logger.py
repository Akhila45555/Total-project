import os
import time
import json
import logging
from dotenv import load_dotenv
from openai import OpenAI
# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def execute_instrumented_llm_call(prompt_text):

    # Input validation
    if not prompt_text.strip():
        print("Prompt cannot be empty.")
        return

    start_time = time.time()

    for attempt in range(3):
        try:
            logging.info(f"Attempt {attempt + 1}: API request started")

            response = client.chat.completions.create(
                model="openrouter/free",
                max_tokens=400,
                messages=[
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ]
            )

            latency = round(time.time() - start_time, 3)

            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens

            telemetry = {
                "status": "SUCCESS",
                "latency_seconds": latency,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens
            }

            if total_tokens > 100:
                logging.warning("High token usage")

            logging.info(
                f"Execution Successful | Latency: {latency}s | Tokens: {total_tokens}"
            )

            print("\n--- Audit Log Telemetry Data ---")
            print(json.dumps(telemetry, indent=4))

            return telemetry

        except Exception as e:
            print(f"Attempt {attempt + 1} failed.")
            print("Error:", e)

            logging.error(f"Attempt {attempt + 1} failed: {e}")

            if attempt == 2:
                print("\nAPI request failed after 3 attempts.")


if __name__ == "__main__":

    prompt = "Explain Artificial Intelligence in simple English."

    execute_instrumented_llm_call(prompt)