import os
import json
import requests

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SNIPEIT_URL = os.getenv("SNIPEIT_URL")
SNIPEIT_TOKEN = os.getenv("SNIPEIT_TOKEN")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing")

if not SNIPEIT_URL:
    raise ValueError("SNIPEIT_URL is missing")

if not SNIPEIT_TOKEN:
    raise ValueError("SNIPEIT_TOKEN is missing")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

MODEL = "openrouter/free"

def search_assets(search_term):

    url = f"{SNIPEIT_URL}/api/v1/hardware"

    headers = {
        "Authorization": f"Bearer {SNIPEIT_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {
        "search": search_term,
        "limit": 5
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

    data = response.json()

    return {
        "success": True,
        "total": data.get("total", 0),
        "assets": data.get("rows", [])
    }


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_assets",
            "description": (
                "Search IT assets in Snipe-IT. "
                "Use this when the user asks to find "
                "a laptop, desktop, hardware asset, "
                "asset tag, serial number or other IT asset."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": (
                            "Asset name, asset tag, "
                            "serial number or search keyword"
                        )
                    }
                },
                "required": ["search_term"]
            }
        }
    }
]

def execute_tool(tool_call):

    tool_name = tool_call.function.name

    arguments = json.loads(
        tool_call.function.arguments
    )

    print("\nTool requested:", tool_name)
    print("Arguments:", arguments)

    if tool_name == "search_assets":

        return search_assets(
            arguments["search_term"]
        )

    return {
        "success": False,
        "error": f"Unknown tool: {tool_name}"
    }

user_request = input(
    "\nAsk about an IT asset: "
)

messages = [
    {
        "role": "user",
        "content": user_request
    }
]



response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message


if not message.tool_calls:

    print("\nLLM Response:")
    print(message.content)

else:

    messages.append(message)

    for tool_call in message.tool_calls:

        result = execute_tool(tool_call)

        print("\nSnipe-IT Result:")
        print(
            json.dumps(
                result,
                indent=2
            )
        )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        )

    final_response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=tools
    )

    final_message = final_response.choices[0].message

    print("\nFinal Answer:")
    print(final_message.content)