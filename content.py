# content.py
from typing import List, Dict, TypedDict, Literal

Dept = Literal["Finance", "Marketing", "Management", "Business Analytics"]

class Choice(TypedDict):
    key: str
    text: str
    presetScore: int

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
        "objective": "Improve internal communications quality and responsiveness with a management chatbot.",
        "choices": [
            {"key":"A","text":"Make everyone answer faster no matter what.", "presetScore":-6},
            {"key":"B","text":"Summarize weekly updates from the last 8 weeks; produce bullet points and action items, maximum 120 words; anonymize any personal data; escalate unresolved items after three exchanges.", "presetScore":7},
            {"key":"C","text":"Make internal communications go viral.", "presetScore":-10}
        ],
        "weights": {"revenue":0.2, "efficiency":0.5, "reputation":0.2, "innovation":0.1}
    },
    {
        "id": 2,
        "department": "Marketing",
        "objective": "Increase click-through rate while protecting brand tone.",
        "choices": [
            {"key":"A","text":"Write edgy copy and ignore the brand guide.", "presetScore":-8},
            {"key":"B","text":"Draft three ad variants for finance students with two headlines each; follow brand style version 2; return a JSON array.", "presetScore":8},
            {"key":"C","text":"Make the ad super clickbait.", "presetScore":-10}
        ],
        "weights": {"revenue":0.4, "efficiency":0.1, "reputation":0.3, "innovation":0.2}
    },
    {
        "id": 3,
        "department": "Finance",
        "objective": "Improve working-capital planning with short-term cash forecasting.",
        "choices": [
            {"key":"A","text":"Forecast cash.", "presetScore":0},
            {"key":"B","text":"Forecast the next eight weeks of cash flows using the past 26 weeks of accounts payable and accounts receivable by category; include 80 percent confidence intervals; flag weeks with root mean square error above 15 percent; output a table.", "presetScore":9},
            {"key":"C","text":"Use competitor internal data if you can find it.", "presetScore":-10}
        ],
        "weights": {"revenue":0.3, "efficiency":0.5, "reputation":0.1, "innovation":0.1}
    },
    {
        "id": 4,
        "department": "Business Analytics",
        "objective": "Reduce stockouts using demand forecasting and alerting.",
        "choices": [
            {"key":"A","text":"Forecast demand for items.", "presetScore":0},
            {"key":"B","text":"Forecast the next eight weeks per SKU using the last 26 weeks; return the top ten stockout risks with drivers and two examples each; include 80 percent confidence intervals.", "presetScore":9},
            {"key":"C","text":"Scrape customer emails to enrich profiles.", "presetScore":-10}
        ],
        "weights": {"revenue":0.2, "efficiency":0.6, "reputation":0.1, "innovation":0.1}
    },
    {
        "id": 5,
        "department": "Marketing",
        "objective": "Plan a compliant, inclusive campus ambassador job post.",
        "choices": [
            {"key":"A","text":"Write a job post for young hustlers only.", "presetScore":-10},
            {"key":"B","text":"Create an inclusive job post for a Campus Ambassador listing skills and growth paths; remove biased language; return bullets and a 120-word summary.", "presetScore":8},
            {"key":"C","text":"Make it aggressive to filter weak candidates.", "presetScore":-6}
        ],
        "weights": {"revenue":0.2, "efficiency":0.2, "reputation":0.4, "innovation":0.2}
    },
    {
        "id": 6,
        "department": "Management",
        "objective": "Final mix: choose any department and tool; craft a prompt aligned to measurable KPIs.",
        "choices": [
            {"key":"A","text":"Summarize the last 12 weeks of relevant data; propose three actions with estimated impact on click-through rate, customer satisfaction, and return on investment; maximum 150 words; exclude personal data; return JSON.", "presetScore":7},
            {"key":"B","text":"Do whatever it takes.", "presetScore":-6},
            {"key":"C","text":"Go viral.", "presetScore":-10}
        ],
        "weights": {"revenue":0.3, "efficiency":0.3, "reputation":0.2, "innovation":0.2}
    }
]
