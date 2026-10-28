"""
Day 37: Agentic Fail-Safe Counter Protection

Objective:
Prevent infinite loops and unnecessary API token costs.

Mechanism:
Stop execution when the agent exceeds 5 consecutive steps.
"""

MAX_ITERATIONS = 5


class AgentCircuitBreaker:
    def __init__(self, max_iterations=MAX_ITERATIONS):
        self.max_iterations = max_iterations
        self.iteration_count = 0
        self.stopped = False

    def execute_step(self):
        if self.stopped:
            print("Agent is already stopped.")
            return False

        if self.iteration_count >= self.max_iterations:
            self.stopped = True
            print("CIRCUIT BREAKER TRIGGERED!")
            print("Maximum iterations exceeded. Agent stopped.")
            return False

        self.iteration_count += 1
        print(f"Executing agent step {self.iteration_count}")

        return True

    def run(self):
        while self.execute_step():
            # Simulate an agent that has not completed its task.
            # In a real agent, execute the actual task here.
            pass

        return False


if __name__ == "__main__":
    agent = AgentCircuitBreaker(max_iterations=5)
    agent.run()