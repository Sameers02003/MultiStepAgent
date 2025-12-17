class LLM:
    """
    Swappable LLM client.
    - For demo: mock deterministic outputs.
    - Real usage: implement OpenAI/Anthropic/Gemini here.
    """
    def __init__(self, provider: str = "mock"):
        self.provider = provider

    def generate(self, prompt: str) -> str:
        # Mock behavior tailored for simple math/time questions
        p = prompt.lower()

        # Planner prompt → numbered plan
        if "numbered plan" in p or "produce a short numbered plan" in p:
            return (
                "1. Parse entities and units\n"
                "2. Extract quantities\n"
                "3. Compute needed values\n"
                "4. Validate constraints\n"
                "5. Format final answer"
            )

        # Executor prompt → intermediate + final
        if "follow the plan" in p:
            return "Intermediate calculations produced.\nFinal Answer: See tool computation."

        # Verifier prompt → approve or reject
        if "strict verifier" in p:
            return "APPROVE"

        return "APPROVE"