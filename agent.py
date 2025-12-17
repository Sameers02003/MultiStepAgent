import re
from prompts import planner_prompt, executor_prompt, verifier_prompt
from tools import solve_with_tools, verify_constraints

class Agent:
    def __init__(self, llm, max_retries=3):
        self.llm = llm
        self.max_retries = max_retries

    def plan(self, question: str):
        prompt = planner_prompt(question)
        raw = self.llm.generate(prompt)
        steps = [line.strip()[3:] for line in raw.strip().split("\n") if line.strip().startswith(tuple("123456789"))]
        return steps

    def execute(self, question: str, steps):
        # Try tool-based solving first
        tool_result = solve_with_tools(question, steps)
        if tool_result and tool_result.get("answer"):
            return tool_result

        # Fallback to LLM execution
        resp = self.llm.generate(executor_prompt(question, steps))
        match = re.search(r'Final Answer:\s*(.+)', resp)
        if match:
            return {
                "answer": match.group(1).strip(),
                "reasoning": resp,
                "proposed_solution": resp
            }
        return {"proposed_solution": resp}

    def verify(self, question: str, proposal):
        prompt = verifier_prompt(question, proposal)
        verdict = self.llm.generate(prompt)
        passed = "approve" in verdict.lower()
        return {
            "check_name": "llm_verifier",
            "passed": passed,
            "details": verdict.strip()
        }

    def solve(self, question: str):
        retries = 0
        while retries < self.max_retries:
            steps = self.plan(question)
            intermediate = self.execute(question, steps)
            answer = intermediate.get("answer")
            reasoning = intermediate.get("reasoning", "")
            checks = []

            # Constraint check
            constraint_check = verify_constraints(question, intermediate)
            checks.append({
                "check_name": "constraints",
                "passed": constraint_check["passed"],
                "details": constraint_check["details"]
            })

            # LLM verifier check
            checks.append(self.verify(question, intermediate))

            if all(c["passed"] for c in checks) and answer:
                return {
                    "answer": answer,
                    "status": "success",
                    "reasoning_visible_to_user": reasoning,
                    "metadata": {
                        "plan": " → ".join(steps),
                        "checks": checks,
                        "retries": retries
                    }
                }

            retries += 1

        return {
            "answer": "",
            "status": "failed",
            "reasoning_visible_to_user": reasoning or "Could not verify a consistent solution within retry budget.",
            "metadata": {
                "plan": " → ".join(steps),
                "checks": checks,
                "retries": retries
            },
            "passed": False,
            "retries": retries
        }