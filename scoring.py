# scoring.py
import re
from typing import Dict, Tuple, List

def score_prompt(p: str) -> Tuple[int, Dict[str, int], bool, List[str], str]:
    """Return (total_score, breakdown, hard_fail, tips, explanation)."""
    text = p.lower()
    breakdown = {"specificity": 0, "clarity": 0, "ethics": 0, "kpi": 0, "tone": 0}
    tips = []
    explanation_parts = []

    # Specificity
    if any(w in text for w in ["month", "data", "analyze", "trend", "report", "summary"]):
        breakdown["specificity"] = 2
        explanation_parts.append("Your prompt included specific data or time details.")
    elif "any" in text or "whatever" in text:
        breakdown["specificity"] = -2
        tips.append("Be specific about what data or examples the AI should use.")
        explanation_parts.append("It was too vague and lacked clear direction.")
    else:
        breakdown["specificity"] = 0

    # Clarity / structure
    if any(w in text for w in ["limit", "short", "3", "three", "list", "bullets", "format"]):
        breakdown["clarity"] = 2
        explanation_parts.append("It gave clear structure or limits to the response.")
    else:
        breakdown["clarity"] = 0

    # Ethics / safety
    if "personal data" in text or "avoid bias" in text or "inclusive" in text:
        breakdown["ethics"] = 2
        explanation_parts.append("It showed awareness of ethics or inclusivity.")
    elif "leak" in text or "private" in text or "hack" in text:
        breakdown["ethics"] = -2
        tips.append("Avoid risky or unethical requests.")
        explanation_parts.append("It risked unethical or unsafe behavior.")
    else:
        breakdown["ethics"] = 0

    # KPI / goal alignment
    if any(w in text for w in ["goal", "improve", "increase", "reduce", "boost", "target"]):
        breakdown["kpi"] = 2
        explanation_parts.append("It connected to measurable goals or outcomes.")
    else:
        breakdown["kpi"] = 0
        tips.append("Tie your prompt to a measurable outcome or goal.")

    # Tone / professionalism
    if any(w in text for w in ["friendly", "clear", "professional", "inclusive", "positive"]):
        breakdown["tone"] = 2
        explanation_parts.append("It used a positive and professional tone.")
    elif any(w in text for w in ["aggressive", "spam", "boring"]):
        breakdown["tone"] = -2
        tips.append("Keep the tone professional and friendly.")
        explanation_parts.append("The tone seemed off or too informal.")
    else:
        breakdown["tone"] = 0

    total = sum(breakdown.values())
    total = max(-10, min(10, total))
    hard_fail = total <= -8

    if hard_fail:
        tips.insert(0, "try again")

    explanation = " ".join(explanation_parts) if explanation_parts else "Rowdy didn’t detect much direction in that prompt."
    return total, breakdown, hard_fail, tips, explanation


def kpi_delta(score: int, weights: Dict[str, float]) -> Dict[str, int]:
    """Convert score to KPI impacts."""
    delta = {}
    for k, w in weights.items():
        delta[k] = round(score * w)
    return delta
