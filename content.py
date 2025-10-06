# content.py  (replace file)
from typing import List, Dict, TypedDict, Literal

Dept = Literal["Finance", "Marketing", "Management", "Business Analytics"]

class Choice(TypedDict):
    key: str
    text: str
    presetScore: int  # -3..+5 typical; no -10 here

class Round(TypedDict):
    id: int
    department: Dept
    objective: str
    choices: List[Choice]
    weights: Dict[str, float]

ROUNDS: List[Round] = [
    {
        "id": 1,
        "department": "Management",
        "objective": "Use a management chatbot to improve clarity and responsiveness of weekly updates.",
        "choices": [
            {"key":"A","text":"Summarize each team’s weekly update into 5 bullets with owners and due dates; limit 120 words; escalate items still open after three cycles.", "presetScore":5},
            {"key":"B","text":"Auto-generate a Slack summary once per week without action owners to keep it lightweight.", "presetScore":2},
            {"key":"C","text":"Aggregate message volume and highlight busiest channels; no content summarization.", "presetScore":0},
        ],
        "weights": {"revenue":0.2, "efficiency":0.5, "reputation":0.2, "innovation":0.1}
    },
    {
        "id": 2,
        "department": "Marketing",
        "objective": "Increase click-through rate while protecting brand tone.",
        "choices": [
            {"key":"A","text":"Create 3 ad variants for finance students; two headlines each; follow brand style v2; return JSON for quick A/B testing.", "presetScore":5},
            {"key":"B","text":"Write one long-form ad focusing on storytelling; allow flexible tone outside the brand guide for creativity.", "presetScore":1},
            {"key":"C","text":"Generate 4 concise variants optimized for accessibility (readability grade ≤ 8) with tone strictly on-brand.", "presetScore":4},
        ],
        "weights": {"revenue":0.4, "efficiency":0.1, "reputation":0.3, "innovation":0.2}
    },
    {
        "id": 3,
        "department": "Finance",
        "objective": "Improve working-capital planning with short-term cash forecasting.",
        "choices": [
            {"key":"A","text":"Forecast next 8 weeks using the past 26 weeks of accounts payable and receivable by category; include 80% confidence intervals and flag high-error weeks (>15% RMSE).", "presetScore":5},
            {"key":"B","text":"Forecast next 4 weeks using the past 8 weeks only to stay more reactive; skip intervals for speed.", "presetScore":2},
            {"key":"C","text":"Provide a trend view of AP/AR and a rule-of-thumb cash buffer instead of a forecast.", "presetScore":0},
        ],
        "weights": {"revenue":0.3, "efficiency":0.5, "reputation":0.1, "innovation":0.1}
    },
    {
        "id": 4,
        "department": "Business Analytics",
        "objective": "Reduce stockouts using demand forecasting and alerting.",
        "choices": [
            {"key":"A","text":"Forecast next 8 weeks per SKU using the last 26 weeks; return top 10 stockout risks with drivers and two examples each; include 80% confidence intervals.", "presetScore":5},
            {"key":"B","text":"Cluster SKUs by velocity and apply one forecast per cluster; faster to compute; no item-level alerts.", "presetScore":3},
            {"key":"C","text":"Provide only descriptive summaries of last quarter’s demand by category.", "presetScore":0},
        ],
        "weights": {"revenue":0.2, "efficiency":0.6, "reputation":0.1, "innovation":0.1}
    },
    {
        "id": 5,
        "department": "Marketing",
        "objective": "Plan a compliant, inclusive campus ambassador job post.",
        "choices": [
            {"key":"A","text":"Create an inclusive job post listing skills and growth paths; remove biased language; output bullets plus a 120-word summary.", "presetScore":5},
            {"key":"B","text":"Write a short, informal post prioritizing humor and personality; review bias later.", "presetScore":1},
            {"key":"C","text":"Provide a skills-only checklist with a neutral tone and no narrative.", "presetScore":2},
        ],
        "weights": {"revenue":0.2, "efficiency":0.2, "reputation":0.4, "innovation":0.2}
    },
    {
        "id": 6,
        "department": "Management",
        "objective": "Final mix: choose any department and tool; craft a prompt aligned to measurable KPIs.",
        "choices": [
            {"key":"A","text":"Summarize the last 12 weeks of relevant data; propose three actions with estimated impact on click-through rate, customer satisfaction, and return on investment; maximum 150 words; exclude personal data; return JSON.", "presetScore":4},
            {"key":"B","text":"Propose one bold initiative with rough impact ranges and a short risk section; narrative only.", "presetScore":2},
            {"key":"C","text":"Provide a diagnostic checklist of inputs needed to decide the next action; no recommendation yet.", "presetScore":1},
        ],
        "weights": {"revenue":0.3, "efficiency":0.3, "reputation":0.2, "innovation":0.2}
    }
]
