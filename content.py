# content.py
from typing import List, Dict, TypedDict, Literal

Dept = Literal["Finance", "Marketing", "Management", "Business Analytics"]

class Choice(TypedDict):
    key: str
    text: str
    kpi_effects: Dict[str, int]  # KPI-specific changes

class Round(TypedDict):
    id: int
    department: Dept
    scenario: str
    objective: str
    choices: List[Choice]


ROUNDS: List[Round] = [
    {
        "id": 1,
        "department": "Marketing",
        "scenario": (
            "You’ve joined a local coffee shop’s marketing team. Sales are steady, but social media engagement is low. "
            "The owners want to use AI to refresh their content strategy without losing their warm, neighborhood tone."
        ),
        "objective": "Use AI to create an authentic campaign that balances creativity, brand consistency, and reach.",
        "choices": [
            {
                "key": "A",
                "text": "Ask AI to analyze customer comments and write friendly captions that reflect real community stories.",
                "kpi_effects": {"revenue": 4, "efficiency": 3, "reputation": 4, "innovation": 2},
            },
            {
                "key": "B",
                "text": "Ask AI to create bold, edgy posts using trending audio to go viral quickly.",
                "kpi_effects": {"revenue": 6, "efficiency": 2, "reputation": 1, "innovation": 4},
            },
            {
                "key": "C",
                "text": "Ask AI to design consistent but plain posts that focus on clear product information only.",
                "kpi_effects": {"revenue": 2, "efficiency": 5, "reputation": 3, "innovation": 0},
            },
        ],
    },
    {
        "id": 2,
        "department": "Finance",
        "scenario": (
            "You’re interning for a student-run meal delivery startup struggling to manage cash flow. "
            "They want AI to forecast spending but are unsure whether to focus on precision, creativity, or speed."
        ),
        "objective": "Use AI to generate a financial forecast that’s accurate, useful, and adaptable.",
        "choices": [
            {
                "key": "A",
                "text": "Ask AI to model future cash flow using the last 6 months of data and project 3 scenarios: best, base, and worst case.",
                "kpi_effects": {"revenue": 5, "efficiency": 4, "reputation": 3, "innovation": 2},
            },
            {
                "key": "B",
                "text": "Ask AI to propose a new forecasting method using unconventional metrics like delivery time or social media sentiment.",
                "kpi_effects": {"revenue": 2, "efficiency": 1, "reputation": 2, "innovation": 6},
            },
            {
                "key": "C",
                "text": "Ask AI to summarize all expenses and income into a simple table without predictions or insights.",
                "kpi_effects": {"revenue": 1, "efficiency": 6, "reputation": 3, "innovation": 0},
            },
        ],
    },
    {
        "id": 3,
        "department": "Management",
        "scenario": (
            "Your student org is preparing for its annual leadership summit. Deadlines are slipping and communication is messy. "
            "You decide to try an AI productivity assistant — but your teammates have mixed feelings about using it."
        ),
        "objective": "Use AI to improve accountability and collaboration without making things feel robotic.",
        "choices": [
            {
                "key": "A",
                "text": "Ask AI to track tasks and automatically message team members when deadlines are approaching.",
                "kpi_effects": {"revenue": 2, "efficiency": 5, "reputation": 2, "innovation": 1},
            },
            {
                "key": "B",
                "text": "Ask AI to create a collaborative dashboard summarizing team progress and highlighting key wins weekly.",
                "kpi_effects": {"revenue": 3, "efficiency": 4, "reputation": 5, "innovation": 3},
            },
            {
                "key": "C",
                "text": "Ask AI to write motivational messages and reflection prompts for team meetings.",
                "kpi_effects": {"revenue": 0, "efficiency": 2, "reputation": 4, "innovation": 4},
            },
        ],
    },
    {
        "id": 4,
        "department": "Business Analytics",
        "scenario": (
            "You’re working on a class project with a retail company. They can’t predict which products sell out fastest. "
            "You’ll use AI to find sales trends and help them plan inventory smarter."
        ),
        "objective": "Leverage AI to find meaningful insights from messy data that improve stock management.",
        "choices": [
            {
                "key": "A",
                "text": "Ask AI to clean and analyze 12 months of sales data, finding trends by season and product type.",
                "kpi_effects": {"revenue": 6, "efficiency": 5, "reputation": 3, "innovation": 2},
            },
            {
                "key": "B",
                "text": "Ask AI to find unusual buying patterns, even if the method is experimental or less tested.",
                "kpi_effects": {"revenue": 3, "efficiency": 2, "reputation": 3, "innovation": 6},
            },
            {
                "key": "C",
                "text": "Ask AI to build visual dashboards summarizing data for executives to interpret manually.",
                "kpi_effects": {"revenue": 2, "efficiency": 4, "reputation": 5, "innovation": 1},
            },
        ],
    },
    {
        "id": 5,
        "department": "Marketing",
        "scenario": (
            "Your college is launching a workshop on AI in Business, and you’re responsible for promoting it. "
            "You’ll use AI to create content that attracts students from different majors."
        ),
        "objective": "Generate creative yet credible outreach posts to maximize workshop attendance.",
        "choices": [
            {
                "key": "A",
                "text": "Ask AI to craft one message per major (business, STEM, arts) that emphasizes real career benefits.",
                "kpi_effects": {"revenue": 5, "efficiency": 3, "reputation": 5, "innovation": 3},
            },
            {
                "key": "B",
                "text": "Ask AI to generate a viral-style meme campaign connecting AI to everyday student life.",
                "kpi_effects": {"revenue": 2, "efficiency": 2, "reputation": 2, "innovation": 7},
            },
            {
                "key": "C",
                "text": "Ask AI to create a short, professional flyer focusing on key event details and times.",
                "kpi_effects": {"revenue": 4, "efficiency": 6, "reputation": 4, "innovation": 1},
            },
        ],
    },
]
