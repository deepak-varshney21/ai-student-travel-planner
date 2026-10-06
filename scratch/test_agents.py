import sys
import os

# Ensure local directory is on path
sys.path.insert(0, os.path.abspath("."))

from agents.orchestrator import TravelPlannerOrchestrator
from tools.budget_calculator import calculate_budget_breakdown
from tools.discount_db import search_discounts
from tools.exporter import generate_markdown_export

def main():
    print("Testing Student Travel Planner Agent System...")
    
    # Test Budget Calculator
    b = calculate_budget_breakdown(500, 5, "Balanced")
    print("Budget breakdown calculated successfully:", b["daily_total_allowance"])
    
    # Test Discount Search
    discounts = search_discounts("Europe")
    print(f"Found {len(discounts)} discounts for Europe.")
    
    # Test Orchestrator
    orchestrator = TravelPlannerOrchestrator()
    plan = orchestrator.generate_full_trip_plan(
        destination="Rome, Italy",
        origin="Berlin, Germany",
        duration=3,
        budget=350,
        currency_label="EUR (€)",
        travel_style="🎒 Backpacker (Extreme Budget)",
        has_student_id=True,
        interests=["🏛️ Art & Museums", "🍕 Foodie & Street Food"]
    )
    
    print("Plan generated successfully!")
    print("Destination:", plan["destination"])
    print("Itinerary days:", len(plan["itinerary"]))
    print("Packing items count:", len(plan["packing_list"]))
    
    md = generate_markdown_export(plan)
    print("Markdown export length:", len(md))
    print("All agent system tests passed!")

if __name__ == "__main__":
    main()
