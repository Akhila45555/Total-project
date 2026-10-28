from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

MAX_ITERATIONS = 5

app = FastAPI(title="Day 37 Agent Fail-Safe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class StartRequest(BaseModel):
    max_iterations: int = Field(default=5, ge=1, le=5)


class AgentCircuitBreaker:
    def __init__(self, max_iterations=MAX_ITERATIONS):
        self.max_iterations = max_iterations
        self.iteration_count = 0
        self.stopped = False
        self.logs = []

    def execute_step(self):
        if self.stopped:
            return False

        if self.iteration_count >= self.max_iterations:
            self.stopped = True
            self.logs.append("CIRCUIT BREAKER TRIGGERED!")
            self.logs.append("Maximum iterations reached. Agent stopped.")
            return False

        self.iteration_count += 1
        self.logs.append(
            f"Executing agent step {self.iteration_count}"
        )
        return True

    def run(self):
        while self.execute_step():
            pass

    def get_status(self):
        return {
            "iteration_count": self.iteration_count,
            "max_iterations": self.max_iterations,
            "stopped": self.stopped,
            "status": "stopped" if self.stopped else "ready",
            "logs": self.logs,
        }


agent = AgentCircuitBreaker()


@app.get("/")
def home():
    return {
        "message": "Day 37 Agent Fail-Safe API is running"
    }


@app.get("/agent/status")
def get_status():
    return agent.get_status()


@app.post("/agent/start")
def start_agent(request: StartRequest):
    global agent

    if agent.iteration_count > 0 or agent.stopped:
        return agent.get_status()

    agent = AgentCircuitBreaker(request.max_iterations)
    agent.run()
    return agent.get_status()


@app.post("/agent/reset")
def reset_agent():
    global agent
    agent = AgentCircuitBreaker()
    return agent.get_status()