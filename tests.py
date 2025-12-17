import os
os.makedirs("logs", exist_ok=True)
import json
from interface import solve

EASY = [
    "If a train leaves at 14:30 and arrives at 18:05, how long is the journey?",
    "3 + 5",
    "Alice has 3 red apples and twice as many green apples as red. How many apples total?",
    "Need 60 minutes. Slots: 09:00–09:30, 09:45–10:30, 11:00–12:00. Which slots fit?",
    "10 + 15"
]

TRICKY = [
    "Train leaves at 18:05 and arrives at 14:30; how long is the journey?",  # arrival before departure
    "Alice has -3 red apples and twice as many green. Total?",                # negative count
    "Need 75 minutes. Slots: 09:00–09:30, 09:45–10:30, 11:00–12:00.",
    "Compute 3 + 5, then add 10 more.",                                       # multi-step arithmetic
    "Meeting needs 60 minutes; slots: 09:00–09:30, 09:45–10:30 (break 15m), 11:00–12:00."
]

def run_suite():
    logs = []
    for q in EASY + TRICKY:
        result = solve(q)
        passed = result["status"] == "success" and bool(result["answer"])
        logs.append({
            "question": q,
            "result": result,
            "passed": passed,
            "retries": result["metadata"]["retries"]
        })
        print(json.dumps(logs[-1], indent=2))

    # Save logs to file
    with open("logs/example_runs.jsonl", "w") as f:
        for entry in logs:
            f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    run_suite()