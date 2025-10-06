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
    scenario: str
    objective: str
    choices: List[Choice]
    weights: Dict[str, float]


ROUNDS: List[Round] = [
    {
        "id": 1,
        "department": "Marketing",
        "scenario": (
            "You’ve joined a university project helping a small coffee shop compete against national chains. "
            "The owners noticed their social media posts barely get any interaction, and they’re losing younger customers. "
            "They want you to use AI to improve their online presence while keeping their local, friendly image intact."
        ),
        "objective": "Use an AI writing tool to design a social media strategy that increases engagement without losing authenticity.",
        "choices": [
            {"key": "A", "text": "Ask the AI to study past posts and write new captions that emphasize the shop’s community feel while testing different post times.", "presetScore": 7},
            {"key": "B", "text": "Ask the AI to create short posts using trending memes to quickly boost likes and shares.", "presetScore": 3},
            {"key": "C", "text": "Ask the AI to write long, formal posts describing every menu item in detail to appear more professional.", "presetScore": 1},
        ],
        "weights": {"revenue": 0.3, "efficiency": 0.3, "reputation": 0.3, "innovation": 0.1},
    },
    {
        "id": 2,
        "department": "Finance",
        "scenario": (
            "You’re interning at a student-run startup that delivers meal kits to dorms. "
            "Cash flow has been tight, and the founders aren’t sure how much money they’ll have left for marketing next month. "
            "They’re tracking everything in spreadsheets but have no forecasting method."
        ),
        "objective": "Use AI to analyze their spending and project cash flow for the next quarter to guide smarter budgeting.",
        "choices": [
            {"key": "A", "text": "Ask the AI to summarize income and expenses, find cost patterns, and simulate how different marketing budgets impact profit.", "presetScore": 7},
            {"key": "B", "text": "Tell the AI to predict profits assuming sales double every month.", "presetScore": 1},
            {"key": "C", "text": "Ask the AI to list transactions from the past month without analyzing trends.", "presetScore": 3},
        ],
        "weights": {"revenue": 0.4, "efficiency": 0.4, "reputation": 0.1, "innovation": 0.1},
    },
    {
        "id": 3,
        "department": "Management",
        "scenario": (
            "Your student organization is hosting its biggest event of the year, but half the team is behind schedule. "
            "You’re considering using an AI assistant to organize deadlines and communication. "
            "Some members worry it might make things too formal or robotic."
        ),
        "objective": "Use AI to improve coordination and accountability while keeping communication personal and motivating.",
        "choices": [
            {"key": "A", "text": "Ask the AI to summarize each member’s progress, identify blockers, and remind people of upcoming deadlines respectfully.", "presetScore": 7},
            {"key": "B", "text": "Ask the AI to send automatic daily alerts for every unfinished task, no matter how small.", "presetScore": 3},
            {"key": "C", "text": "Ask the AI to draft motivational messages each week without tracking actual work progress.", "presetScore": 2},
        ],
        "weights": {"revenue": 0.1, "efficiency": 0.5, "reputation": 0.2, "innovation": 0.2},
    },
    {
        "id": 4,
        "department": "Business Analytics",
        "scenario": (
            "Your class is working with a regional clothing brand that can’t predict which products will sell out. "
            "They’ve collected tons of data but don’t know how to use it effectively. "
            "You’re tasked with showing how AI can turn raw data into smarter inventory decisions."
        ),
        "objective": "Use AI to analyze sales data and recommend which items to restock next season.",
        "choices": [
            {"key": "A", "text": "Ask the AI to group sales data by item category, compare seasonal trends, and suggest which items to restock.", "presetScore": 7},
            {"key": "B", "text": "Ask the AI to create a colorful graph of sales totals without context or recommendations.", "presetScore": 3},
            {"key": "C", "text": "Ask the AI to estimate future demand using only average sales numbers from one month.", "presetScore": 2},
        ],
        "weights": {"revenue": 0.3, "efficiency": 0.4, "reputation": 0.2, "innovation": 0.1},
    },
    {
        "id": 5,
        "department": "Marketing",
        "scenario": (
            "Your university’s business department is launching an AI in Business workshop, and they want help promoting it. "
            "The goal is to attract students from all majors, not just business. "
            "They’ve asked you to test whether AI can write creative but professional outreach messages."
        ),
        "objective": "Use AI to write an engaging announcement that gets students to sign up without overhyping the event.",
        "choices": [
            {"key": "A", "text": "Ask the AI to write three short announcements tailored to different audiences (STEM, Arts, Business) with unique benefits for each.", "presetScore": 7},
            {"key": "B", "text": "Ask the AI to write one post filled with industry buzzwords like 'revolutionary' and 'game-changing'.", "presetScore": 2},
            {"key": "C", "text": "Ask the AI to write a long paragraph explaining the history of AI with no clear call-to-action.", "presetScore": 3},
        ],
        "weights": {"revenue": 0.2, "efficiency": 0.3, "reputation": 0.3, "innovation": 0.2},
    },
    {
        "id": 6,
        "department": "Management",
        "scenario": (
            "You’re consulting for a nonprofit that’s struggling to keep track of project results. "
            "The team wants to learn from mistakes but lacks time to review reports from past initiatives. "
            "They’ve asked you to experiment with using AI for knowledge sharing."
        ),
        "objective": "Use AI to summarize lessons from past projects and create insights the team can use for planning.",
        "choices": [
            {"key": "A", "text": "Ask the AI to summarize past reports, list successes and failures, and provide three improvement ideas.", "presetScore": 7},
            {"key": "B", "text": "Ask the AI to create a single summary of results without recommendations.", "presetScore": 3},
            {"key": "C", "text": "Ask the AI to make a client list and completion dates for quick reference only.", "presetScore": 2},
        ],
        "weights": {"revenue": 0.1, "efficiency": 0.3, "reputation": 0.3, "innovation": 0.3},
    },
]
