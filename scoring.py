# scoring.py
import re
from typing import Dict, List, Tuple

ScoreBreakdown = Dict[str, int]

def score_prompt(text: str) -> Tuple[int, ScoreBreakdown, bool, List[str]]:
    lc = text.lower()
    bd: ScoreBreakdown = {"specificity":0, "data":0, "constraints":0, "ethics":0, "kpi":0}
    tips: List[str] = []

    # Specificity
    if re.search(r"\b(top|3|three)\b.*\bissues?\b", lc) or re.search(r"\bexamples?\b", lc) or "json" in lc:
        bd["specificity"] = 2
    elif re.search(r"\b(improve|analyze|optimize|forecast|summarize)\b", lc):
        bd["specificity"] = 0
    else:
        bd["specificity"] = -2

    # Data anchoring
    if re.search(r"\b(last|past)\s+\d+\s+(weeks|months|quarters|years)\b", lc) or "by sku" in lc:
        bd["data"] = 2
    elif "data" in lc:
        bd["data"] = 0
    elif re.search(r"\bpublic|scrape\b", lc):
        bd["data"] = -2
        tips.append("Anchor to owned/authorized data, not scraping.")
    else:
        bd["data"] = 0

    # Constraints / format
    if re.search(r"\bmax\s*\d+\s*(words|chars)\b", lc) or any(x in lc for x in ["json","table","bullet","bullets"]) or re.search(r"\bescalat(e|ion)\b", lc):
        bd["constraints"] = 2
    elif re.search(r"do whatever it takes|as much as possible", lc):
        bd["constraints"] = -2
        tips.append("Add clear format and guardrails.")
    else:
        bd["constraints"] = 0

    # Ethics/compliance
    if re.search(r"\bexclude\b.*\bpii\b", lc) or "anonymize" in lc or re.search(r"\bbias(ed)?-?free\b", lc):
        bd["ethics"] = 2
    elif re.search(r"scrape customer emails|use competitor internal data|young", lc):
        bd["ethics"] = -2
        tips.append("Avoid risky, biased, or non-compliant instructions.")
    else:
        bd["ethics"] = 0

    # KPI alignment (no abbreviations)
    if re.search(r"\b(customer satisfaction|average handle time|click[- ]through rate|return on investment|root mean square error|confidence interval|80%|net present value|return on assets|return on equity|customer acquisition cost|lifetime value)\b", lc):
        bd["kpi"] = 2
    elif "viral" in lc:
        bd["kpi"] = -2
        tips.append("Tie prompts to measurable business KPIs.")
    else:
        bd["kpi"] = 0

    total = sum(bd.values())
    total = max(-10, min(10, total))
    hard_fail = (total == -10)

    if hard_fail:
        tips = ["try again"]
    elif total < 0 and not tips:
        tips.append("Add time range for data, clear output format, and explicit KPI targets.")

    return total, bd, hard_fail, tips


def kpi_delta(score: int, weights: Dict[str, float]) -> Dict[str, int]:
    return {
        "revenue": round(score * weights["revenue"]),
        "efficiency": round(score * weights["efficiency"]),
        "reputation": round(score * weights["reputation"]),
        "innovation": round(score * weights["innovation"]),
    }
