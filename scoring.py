# scoring.py
from typing import Dict, Tuple, List

def score_prompt(p: str) -> Tuple[int, Dict[str, int], bool, List[str], str]:
    """Return (total_score, breakdown, hard_fail, tips, explanation)."""
    text = p.lower()
    breakdown = {"specificity": 0, "clarity": 0, "ethics": 0, "kpi": 0, "tone": 0}
    tips, explanation_parts = [], []

    # Specificity
    if any(w in text for w in ["data", "trend", "report", "forecast", "month", "analyze"]):
        breakdown["specificity"] = 2
        explanation_parts.append("Your prompt included data details or time ranges, showing precision.")
    elif "random" in text or "whatever" in text:
        breakdown["specificity"] = -2
        tips.append("Be clear about what information the AI should analyze.")
        explanation_parts.append("It lacked clear direction or focus.")

    # Clarity
    if any(w in text for w in ["short", "three", "list", "steps", "format", "limit"]):
        breakdown["clarity"] = 2
        explanation_parts.append("You structured the task clearly, making it easy for AI to follow.")
    else:
        tips.append("Consider giving structure — like lists or limits — for clarity.")

    # Ethics / tone
    if any(w in text for w in ["ethical", "safe", "inclusive", "positive", "respectful"]):
        breakdown["ethics"] = 2
        explanation_parts.append("Your prompt showed awareness of tone and inclusivity.")
    elif any(w in text for w in ["private", "leak", "bias"]):
        breakdown["ethics"] = -2
        explanation_parts.append("It risked ethical issues or unclear tone.")
        tips.append("Always promote safe, respectful outputs.")

    # KPI / goals
    if any(w in text for w in ["goal", "improve", "increase", "reduce", "optimize", "measure"]):
        breakdown["kpi"] = 2
        explanation_parts.append("You linked actions to measurable outcomes.")
    else:
        tips.append("Try connecting your prompt to a specific measurable goal.")

    total = sum(breakdown.values())
    hard_fail = total <= -6
    explanation = " ".join(explanation_parts) if explanation_parts else "Rowdy couldn’t find much direction in that prompt."

    return total, breakdown, hard_fail, tips, explanation


def kpi_delta(score: int, weights: Dict[str, float]) -> Dict[str, int]:
    delta = {}
    for k, w in weights.items():
        delta[k] = round(score * w)
    return delta
