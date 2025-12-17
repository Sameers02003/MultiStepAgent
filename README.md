# Multi-Step Reasoning Agent with Self-Checking

## 🧠 Overview
This agent solves structured word problems using a 3-phase loop:
1. **Planner** — breaks the question into steps.
2. **Executor** — runs the steps using tools or LLM.
3. **Verifier** — checks the result and retries if needed.

It returns a clean JSON with:
- `answer`: final short answer
- `status`: success or failed
- `reasoning_visible_to_user`: short explanation
- `metadata`: internal plan, checks, and retry count

---

## 🚀 How to Run

### CLI
```bash
python interface.py

~~~~Type any Question like: ~~~~~

1. If a train leaves at 14:30 and arrives at 18:05, how long is the journey?

~~~Tests:
Python tests.py

~~~Folder Structure:

MultiStepAgent/
├── agent.py
├── prompts.py
├── llm.py
├── tools.py
├── interface.py
├── tests.py
├── logs/
│   └── example_runs.jsonl
└── README.md

~~Logs saved to :


---

### 4. **Improvements (Optional but impressive)**
Add a short note like:
```markdown
### 🔧 Future Improvements
- Add few-shot examples to prompts
- Use real LLM API with temperature control
- Add richer constraint checks (e.g. overlapping slots)
- Deploy with FastAPI for web demo
