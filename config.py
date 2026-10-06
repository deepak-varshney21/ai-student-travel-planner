import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

# Gemini Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# Application Settings
APP_TITLE = "🎓 Student Travel Planner AI"
APP_TAGLINE = "Multi-Agent Smart Trip Orchestrator for Budget-Conscious Student Travelers"

# Student Travel Categories
TRAVEL_STYLES = [
    "🎒 Backpacker (Extreme Budget)",
    "⚖️ Balanced Student (Smart Spend)",
    "✨ Comfort & Culture (Splurge a bit)",
    "🏔️ Adventure & Outdoors",
    "🎨 Nightlife & Culture Explorer"
]

CURRENCIES = {
    "USD ($)": "$",
    "EUR (€)": "€",
    "GBP (£)": "£",
    "INR (₹)": "₹",
    "CAD ($)": "CA$",
    "AUD ($)": "A$",
    "JPY (¥)": "¥"
}
