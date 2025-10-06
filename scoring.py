# scoring.py
from typing import Dict, Tuple, List

def interpret_kpis(delta: Dict[str, int]) -> str:
    """Convert KPI changes into a readable explanation."""
    insights = []
    for k, v in delta.items():
        if v > 4:
            insights.append(f"strong in {k}")
        elif v > 2:
            insights.append(f"solid improvement in {k}")
        elif v > 0:
            insights.append(f"minor progress in {k}")
        elif v < 0:
            insights.append(f"weaker in {k}")
    return ", ".join(insights) if insights else "no significant changes."

def score_prompt(p: str) -> Tuple[int, Dict[str, int], bool, List[str], str]:
    """Return (total_score, breakdown, hard_fail, tips, explanation)."""
    text = p.lower()
    score = 0
    tips, explanation_parts = [], []

    if "data" in text or "analyze" in text:
        score += 3
        explanation_parts.append("You focused on data-driven reasoning.")
    if "goal" in text or "improve" in text:
        score += 2
        explanation_parts.append("You linked your prompt to measurable outcomes.")
    if "inclusive" in text or "positive" in text:
        score += 1
        explanation_parts.append("You kept tone and inclusivity in mind.")
    if "random" in text or "guess" in text:
        score -= 3
        explanation_parts.append("You used uncertain or unstructured language.")

    hard_fail = score <= -5
    explanation = " ".join(explanation_parts) if explanation_parts else "Rowdy didn’t detect much direction in that prompt."
    return score, {}, hard_fail, tips, explanation
