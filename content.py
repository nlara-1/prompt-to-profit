# content.py
from typing import List, Dict, TypedDict, Literal

Dept = Literal["Finance", "Marketing", "Management", "Business Analytics"]

class Choice(TypedDict):
    key: str
    text: str
    presetScore: int  # from -3 to +5 typical

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
            "Your campus consulting club just took on a project for a small local coffee shop that wants to boost its online visibility. "
            "They’re using social media but aren’t sure what kind of messaging connects best with students."
        ),
        "objective": "Use an AI writing assistant to help the coffee shop increase engagement on Instagram while keeping the brand authentic.",
        "choices": [
            {"key": "A", "text": "Ask the AI to write three sample Instagram captions using a friendly and inclusive tone. Include call-to-actions like tagging friends or sharing experiences.", "presetScore": 5},
            {"key": "B", "text": "Tell the AI to make five quick posts with trending memes and hashtags for maximum clicks.", "presetScore": 0},
            {"key": "C", "text": "Request one long, formal post explaining the shop’s history and values in detail.", "presetScore": 2},
        ],
        "weights": {"revenue": 0.4, "efficiency": 0.2, "reputation": 0.3, "innovation": 0.1},
    },
    {
        "id": 2,
        "department": "Finance",
        "scenario": (
            "You’ve joined an internship with a startup that needs help understanding its cash flow. "
            "The founder tracks spending manually and often runs out of funds near the end of the month."
        ),
        "objective": "Use an AI data helper to forecast how much money the startup will have left each month for the next quarter.",
        "choices": [
            {"key": "A", "text": "Ask the AI to analyze the past three months of income and expenses, highlight spending trends, and show which costs could be reduced.", "presetScore": 5},
            {"key": "B", "text": "Tell the AI to list every transaction without summarizing or suggesting any changes.", "presetScore": 1},
            {"key": "C", "text": "Ask the AI to predict next quarter’s cash flow using random estimates since detailed data isn’t available.", "presetScore": 0},
        ],
        "weights": {"revenue": 0.3, "efficiency": 0.4, "reputation": 0.2, "innovation": 0.1},
    },
    {
        "id": 3,
        "department": "Management",
        "scenario": (
            "You’re helping lead a student organization preparing for a big event. Communication has been messy, and members keep missing deadlines. "
            "You decide to bring in an AI assistant to help with coordination."
        ),
        "objective": "Use AI to make communication smoother and improve accountability among team members.",
        "choices": [
            {"key": "A", "text": "Ask the AI to summarize weekly updates from members and generate a checklist with deadlines and who’s responsible for each task.", "presetScore": 5},
            {"key": "B", "text": "Tell the AI to post daily reminders in the group chat for every small task.", "presetScore": 2},
            {"key": "C", "text": "Have the AI draft motivational quotes to boost morale without tracking actual work progress.", "presetScore": 0},
        ],
        "weights": {"revenue": 0.1, "efficiency": 0.5, "reputation": 0.2, "innovation": 0.2},
    },
    {
        "id": 4,
        "department": "Business Analytics",
        "scenario": (
            "Your business class is running a simulation for a clothing brand. "
            "The company struggles to predict which items will sell out and which will stay on the shelf."
        ),
        "objective": "Use an AI data tool to help the company make better restock decisions before each season.",
        "choices": [
            {"key": "A", "text": "Ask the AI to review sales data from the past year, identify the top-selling styles, and forecast demand for each item type.", "presetScore": 5},
            {"key": "B", "text": "Tell the AI to give general fashion advice without using the company’s sales numbers.", "presetScore": 0},
            {"key": "C", "text": "Request that the AI create a graph of total sales but skip recommendations or patterns.", "presetScore": 2},
        ],
        "weights": {"revenue": 0.3, "efficiency": 0.4, "reputation": 0.2, "innovation": 0.1},
    },
    {
        "id": 5,
        "department": "Marketing",
        "scenario": (
            "Your school’s career center wants to promote a new workshop on AI in business. "
            "They’ve asked you to test how well an AI can write promotional content that encourages student sign-ups."
        ),
        "objective": "Use an AI copywriter to design a clear, inclusive workshop announcement that feels engaging but professional.",
        "choices": [
            {"key": "A", "text": "Ask the AI to write three short promotional posts tailored for students from different majors, each with a friendly tone and a clear benefit.", "presetScore": 5},
            {"key": "B", "text": "Tell the AI to write one post full of buzzwords like ‘disruptive’ and ‘game-changing’ for extra excitement.", "presetScore": 1},
            {"key": "C", "text": "Ask the AI to create a long essay describing why AI is important in business, without a call-to-action.", "presetScore": 0},
        ],
        "weights": {"revenue": 0.2, "efficiency": 0.3, "reputation": 0.3, "innovation": 0.2},
    },
    {
        "id": 6,
        "department": "Management",
        "scenario": (
            "You’ve been hired as a project coordinator for a small consulting team. "
            "Your manager wants to see how you can use AI to improve how the team learns from past projects."
        ),
        "objective": "Use an AI assistant to summarize lessons from past projects and help the team make better decisions next time.",
        "choices": [
            {"key": "A", "text": "Ask the AI to summarize the last three projects, highlight what went well, what didn’t, and provide three improvement ideas.", "presetScore": 5},
            {"key": "B", "text": "Ask the AI to create a detailed project summary without noting what could be improved.", "presetScore": 2},
            {"key": "C", "text": "Tell the AI to list client names and project dates only.", "presetScore": 0},
        ],
        "weights": {"revenue": 0.1, "efficiency": 0.3, "reputation": 0.3, "innovation": 0.3},
    },
]
