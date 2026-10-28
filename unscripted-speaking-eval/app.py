from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from speaking import run_evaluation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Day 21 Speaking Evaluation API is running"
    }


@app.post("/evaluate")
def evaluate():

    topic = "What is Generative AI?"

    result = run_evaluation(
        topic=topic,
        duration=60
    )

    return result