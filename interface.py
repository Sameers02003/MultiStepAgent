import json
from agent import Agent
from llm import LLM

def solve(question: str) -> dict:
    """Main function to solve a question using the Agent."""
    agent = Agent(llm=LLM(), max_retries=2)
    return agent.solve(question)

if __name__ == "__main__":
    print("Type a question (or 'exit' to quit):")
    while True:
        q = input("> ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        result = solve(q)
        print(json.dumps(result, indent=2))