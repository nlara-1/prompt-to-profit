# content.py
from typing import List, Dict, TypedDict, Literal

Dept = Literal["Finance", "Marketing", "Management", "Business Analytics"]

class Choice(TypedDict):
    key: str
    text: str
    kpi_effects: Dict[str, int]

class Round(TypedDict):
    id: int
    department: Dept
    scenario: str
    objective: str
    priority: str  # which KPI is most important
    choices: List[Choice]


ROUNDS: List[Round] = [
    {
        "id": 1,
        "department": "Marketing",
        "scenario": (
            "Your campus coffee shop just launched a rewards app, but student downloads are slow. "
            "The manager wants quick growth before finals week when students will spend more."
        ),
        "objective": "Use AI to design a campaign that drives engagement without harming the brand image.",
        "priority": "revenue",
        "choices": [
            {
                "key": "A",
                "text": "Ask AI to analyze existing customers and create personalized deals to boost short-term sales.",
                "kpi_effects": {"revenue": 6, "efficiency": 4, "reputation": 2, "innovation": 1},
            },
            {
                "key": "B",
                "text": "Ask AI to design a viral challenge on social media around sustainability and reusable cups.",
                "kpi_effects": {"revenue": 3, "efficiency": 2, "reputation": 5, "innovation": 5},
            },
            {
                "key": "C",
                "text": "Ask AI to build a survey to better understand why students haven’t downloaded the app yet.",
                "kpi_effects": {"revenue": 2, "efficiency": 3, "reputation": 4, "innovation": 2},
            },
        ],
    },
    {
        "id": 2,
        "department": "Finance",
        "scenario": (
            "You’re interning at a startup that’s struggling to manage cash flow after a new product launch. "
            "The CFO wants a clear forecast before presenting to investors next week."
        ),
        "objective": "Use AI to forecast next quarter’s cash position while balancing speed and accuracy.",
        "priority": "efficiency",
        "choices": [
            {
                "key": "A",
                "text": "Use AI to generate three financial models (best, base, worst) from historical spending data.",
                "kpi_effects": {"revenue": 5, "efficiency": 5, "reputation": 4, "innovation": 2},
            },
            {
                "key": "B",
                "text": "Ask AI to include alternative data like customer sentiment and delivery times to refine projections.",
                "kpi_effects": {"revenue": 3, "efficiency": 2, "reputation": 3, "innovation": 6},
            },
            {
                "key": "C",
                "text": "Ask AI to simplify the report into visuals with quick key takeaways for investor readability.",
                "kpi_effects": {"revenue": 4, "efficiency": 6, "reputation": 5, "innovation": 1},
            },
        ],
    },
    {
        "id": 3,
        "department": "Management",
        "scenario": (
            "Your student consulting group is falling behind on deliverables. "
            "The president asks you to use AI tools to organize project tasks and communication."
        ),
        "objective": "Use AI to restore accountability without making your team feel micromanaged.",
        "priority": "reputation",
        "choices": [
            {
                "key": "A",
                "text": "Ask AI to track deliverables and send automated reminders before deadlines.",
                "kpi_effects": {"revenue": 2, "efficiency": 5, "reputation": 3, "innovation": 1},
            },
            {
                "key": "B",
                "text": "Ask AI to build a dashboard showing task ownership, progress trends, and weekly highlights.",
                "kpi_effects": {"revenue": 3, "efficiency": 4, "reputation": 6, "innovation": 3},
            },
            {
                "key": "C",
                "text": "Ask AI to analyze team mood and generate motivational summaries after meetings.",
                "kpi_effects": {"revenue": 1, "efficiency": 2, "reputation": 5, "innovation": 5},
            },
        ],
    },
    {
        "id": 4,
        "department": "Business Analytics",
        "scenario": (
            "A retail chain wants to predict which products will run out before holiday season. "
            "Your job is to use AI insights to help them avoid stockouts without over-ordering inventory."
        ),
        "objective": "Use AI to create a balanced forecast that improves inventory accuracy.",
        "priority": "revenue",
        "choices": [
            {
                "key": "A",
                "text": "Ask AI to analyze 12 months of sales data by region, price, and product category.",
                "kpi_effects": {"revenue": 6, "efficiency": 5, "reputation": 3, "innovation": 2},
            },
            {
                "key": "B",
                "text": "Ask AI to search for unusual buying spikes using external factors like weather and campus events.",
                "kpi_effects": {"revenue": 3, "efficiency": 2, "reputation": 3, "innovation": 6},
            },
            {
                "key": "C",
                "text": "Ask AI to summarize data into visual dashboards for store managers to interpret manually.",
                "kpi_effects": {"revenue": 2, "efficiency": 4, "reputation": 5, "innovation": 1},
            },
        ],
    },
    {
        "id": 5,
        "department": "Marketing",
        "scenario": (
            "You’re leading promotions for your university’s first AI in Business Summit. "
            "The dean expects full attendance, but student interest seems low so far."
        ),
        "objective": "Use AI to boost event attendance while keeping messaging professional.",
        "priority": "innovation",
        "choices": [
            {
                "key": "A",
                "text": "Ask AI to write targeted LinkedIn-style posts featuring career benefits of attending.",
                "kpi_effects": {"revenue": 4, "efficiency": 4, "reputation": 6, "innovation": 2},
            },
            {
                "key": "B",
                "text": "Ask AI to create a student-focused meme campaign connecting AI to campus life humor.",
                "kpi_effects": {"revenue": 3, "efficiency": 3, "reputation": 3, "innovation": 7},
            },
            {
                "key": "C",
                "text": "Ask AI to design one clean promotional email summarizing event details and RSVP info.",
                "kpi_effects": {"revenue": 4, "efficiency": 6, "reputation": 4, "innovation": 1},
            },
        ],
    },
]
