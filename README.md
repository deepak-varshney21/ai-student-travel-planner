# 🎓 Student Travel Planner AI Agent System

A multi-agent AI travel planning ecosystem designed specifically for budget-conscious university and college students. Built with **Google GenAI (Gemini 2.5 Flash)** and **Streamlit**.

---

## 🌟 Key Features

- **🤖 Multi-Agent AI Architecture:**
  - **Lead Orchestrator Agent (`orchestrator.py`):** Coordinates specialized sub-agents and synthesizes executive travel blueprints.
  - **Itinerary Planning Agent (`itinerary_agent.py`):** Crafts day-by-day student routes, free museum days, local food spots, and walkable schedules.
  - **Budget & Discount Management Agent (`budget_agent.py`):** Calculates category breakdowns, daily spend allowances, hostel targets, and student discount savings (ISIC, Railcards, StudentUniverse).
  - **Packing & Safety Advisor Agent (`packing_safety_agent.py`):** Generates minimalist packing checklists and essential student safety/scam warnings.
- **📊 Interactive Visual Analytics:**
  - Dynamic Plotly budget pie charts and student savings comparison bar charts.
- **🏷️ Global Student Discount Directory:**
  - Built-in searchable tool for verified student discounts on flights, trains, hostels, and museum entries worldwide.
- **💬 Real-Time Conversational AI Advisor:**
  - Context-aware chatbot to answer student travel questions on demand.
- **📄 Printable Export:**
  - Export trip itineraries to Markdown (`.md`) and styled HTML (`.html`) printable blueprints.

---

## 🏗️ Architecture Overview

```
modest-volta/
├── app.py                     # Streamlit multi-tab web application
├── config.py                  # Environment & model settings
├── requirements.txt           # Dependencies
├── .env.example               # Template for GEMINI_API_KEY
├── agents/
│   ├── base_agent.py          # Google GenAI SDK wrapper (gemini-2.5-flash)
│   ├── itinerary_agent.py     # Day-by-day student schedule generator
│   ├── budget_agent.py        # Financial breakdown & discount analyzer
│   ├── packing_safety_agent.py# Packing checklist & safety specialist
│   └── orchestrator.py        # Master Orchestrator & Chat Advisor
├── tools/
│   ├── budget_calculator.py   # Math breakdown & Plotly charts generator
│   ├── discount_db.py         # Student discount database & search tool
│   └── exporter.py            # Markdown & HTML export formatter
└── assets/
    └── style.css              # Custom CSS styling
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Gemini API Key (Optional)
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```
*Note: If no API key is provided, the application runs in **Smart Demo/Offline Mode** with heuristic fallback generators.*

### 3. Launch the Streamlit Web Application
```bash
streamlit run app.py
```

The web dashboard will launch automatically at `http://localhost:8501`.

---

## 🎨 Application Screenshots & Views

1. **🗺️ AI Trip Planner:** Input origin, destination, duration, budget, and travel style to launch the multi-agent workflow.
2. **💸 Student Discount Explorer:** Search student deals on Eurail, Amtrak, ISIC, Hostels, and free museum entries.
3. **💬 AI Travel Advisor Chat:** Ask live travel questions or choose from quick preset starter prompts.
4. **📄 Export & Save:** Download markdown and printable HTML itinerary blueprints.
