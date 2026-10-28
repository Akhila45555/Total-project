mock_response = {
    "content": [
        {
            "text": "Python is a programming language."
        }
    ],
    "usage": {
        "input_tokens": 45,
        "output_tokens": 120
    }
}

content = mock_response.get("content", [])

if content:
    text = content[0].get("text", "")
else:
    text = ""

print("Response:")
print(text)

usage = mock_response.get("usage", {})

input_tokens = usage.get("input_tokens", 0)
output_tokens = usage.get("output_tokens", 0)

total_tokens = input_tokens + output_tokens

print("\nMetadata")
print("Input Tokens:", input_tokens)
print("Output Tokens:", output_tokens)
print("Total Tokens:", total_tokens)