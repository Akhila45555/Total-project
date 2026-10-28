"""
Day 44: Technical Mock Panels
Purpose: Practice GenAI prompts, API routing, and security.
"""

questions = [
    {
        "topic": "GenAI Prompt Mechanics",
        "question": "What is a prompt in GenAI?",
        "keywords": ["instruction", "model"],
        "sample_answer": (
            "A prompt is an instruction given to an AI model "
            "to generate a relevant response."
        )
    },
    {
        "topic": "GenAI Prompt Mechanics",
        "question": "Why should prompts be clear?",
        "keywords": ["clear", "accurate"],
        "sample_answer": (
            "Clear prompts help the model generate more "
            "relevant and accurate responses."
        )
    },
    {
        "topic": "API Routing",
        "question": "What is API routing?",
        "keywords": ["endpoint", "request"],
        "sample_answer": (
            "API routing directs a request to the correct "
            "backend endpoint."
        )
    },
    {
        "topic": "API Routing",
        "question": "What is the difference between GET and POST?",
        "keywords": ["retrieve", "send"],
        "sample_answer": (
            "GET is commonly used to retrieve data, while "
            "POST is commonly used to send data to a server."
        )
    },
    {
        "topic": "Security",
        "question": "Why should API keys be kept secret?",
        "keywords": ["unauthorized", "access"],
        "sample_answer": (
            "API keys should be protected to prevent "
            "unauthorized access and misuse."
        )
    },
    {
        "topic": "Security",
        "question": "What is PII masking?",
        "keywords": ["personal", "sensitive"],
        "sample_answer": (
            "PII masking hides or replaces sensitive personal "
            "information before it is shared."
        )
    }
]


def evaluate_answer(answer, keywords):
    answer = answer.lower()
    matched = [
        word for word in keywords
        if word in answer
    ]
    return len(matched)


def run_mock_panel():
    print("=" * 50)
    print("DAY 44 - TECHNICAL MOCK PANELS")
    print("=" * 50)

    candidate = input("Enter candidate name: ").strip()

    if not candidate:
        candidate = "Candidate"

    total_score = 0
    max_score = 0
    report = []

    for number, item in enumerate(questions, start=1):
        print(f"\nQuestion {number}: {item['question']}")
        print(f"Topic: {item['topic']}")

        answer = input("Your answer: ").strip()

        score = evaluate_answer(
            answer, item["keywords"]
        )
        maximum = len(item["keywords"])

        total_score += score
        max_score += maximum

        report.append({
            "topic": item["topic"],
            "question": item["question"],
            "score": score,
            "maximum": maximum,
            "sample": item["sample_answer"]
        })

    percentage = (
        total_score / max_score * 100
        if max_score else 0
    )

    print("\n" + "=" * 50)
    print("TECHNICAL MOCK PANEL REPORT")
    print("=" * 50)
    print(f"Candidate: {candidate}")
    print(f"Keyword score: {total_score}/{max_score}")
    print(f"Keyword match: {percentage:.1f}%")

    print("\nTOPIC-WISE FEEDBACK")

    for item in report:
        print(f"\nTopic: {item['topic']}")
        print(f"Question: {item['question']}")
        print(
            f"Score: {item['score']}/"
            f"{item['maximum']}"
        )
        print(f"Reference answer: {item['sample']}")

    print("\nMock interview completed.")
    print("Use the feedback to improve your answers.")


if __name__ == "__main__":
    run_mock_panel()