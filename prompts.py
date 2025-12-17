def planner_prompt(question: str) -> str:
    return f"""You are a precise planner. Given the question, produce a short numbered plan.
- Use 3–6 steps.
- Each step should be atomic and actionable.
Question: {question}
Output format:
1. Parse entities and units
2. Extract quantities
3. Compute needed values
4. Validate constraints
5. Format final answer"""

def executor_prompt(question: str, steps) -> str:
    steps_text = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
    return f"""Follow the plan strictly and show intermediate calculations.
Question: {question}
Plan:
{steps_text}
Return a concise final answer at the end, and include a brief reasoning summary."""

def verifier_prompt(question: str, proposal) -> str:
    return f"""You are a strict verifier.
Given the question and proposed solution (answer and reasoning), check for:
- Math correctness
- Unit/time sanity
- Non-negative counts and logical constraints
Either say 'APPROVE' if consistent, or explain issues.
Question: {question}
Proposal: {proposal}"""