from dataclasses import dataclass

@dataclass
class ContextBudget:
    context_window: int
    system_tokens: int
    history_tokens: int
    prompt_tokens: int
    reserved_output_tokens: int

    @property
    def input_tokens(self):
        return self.system_tokens + self.history_tokens + self.prompt_tokens

    @property
    def available_input(self):
        return max(0, self.context_window - self.reserved_output_tokens)

    @property
    def remaining(self):
        return self.context_window - self.reserved_output_tokens - self.input_tokens

    @property
    def fits(self):
        return self.remaining >= 0

def calculate_budget(context_window: int, system_tokens: int, history_tokens: int,
                     prompt_tokens: int, reserved_output_tokens: int) -> ContextBudget:
    values = [context_window, system_tokens, history_tokens, prompt_tokens, reserved_output_tokens]
    if any(not isinstance(v, int) for v in values):
        raise TypeError("All budget values must be integers")
    if context_window < 0 or min(system_tokens, history_tokens, prompt_tokens, reserved_output_tokens) < 0:
        raise ValueError("Token counts cannot be negative")
    if reserved_output_tokens > context_window:
        raise ValueError("Reserved output cannot exceed the context window")
    return ContextBudget(*values)

def assess_prompt(prompt: str, token_count: int, budget: int, required_terms: list[str]) -> dict:
    """Transparent heuristic: fit + objective phrase + essential concepts. Not semantic AI evaluation."""
    normalized = prompt.casefold()
    matched = [term for term in required_terms if term.casefold() in normalized]
    coverage = len(matched) / len(required_terms) if required_terms else 1.0
    fits = token_count <= budget
    passed = fits and coverage >= 0.6
    return {"passed": passed, "fits": fits, "matched": matched,
            "coverage": round(coverage, 2),
            "feedback": ("Fits the budget and preserves the core requirements." if passed else
                         "Revise: the prompt must fit the budget and retain at least 60% of the listed essential concepts.")}
