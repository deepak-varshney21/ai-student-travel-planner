"""
Master Multi-Agent Orchestrator
Coordinates ItineraryAgent, BudgetAgent, and PackingSafetyAgent to generate complete travel packages and handle interactive travel chat queries.
"""

import logging
from agents.base_agent import BaseAgent
from agents.itinerary_agent import ItineraryAgent
from agents.budget_agent import BudgetAgent
from agents.packing_safety_agent import PackingSafetyAgent
from config import CURRENCIES

logger = logging.getLogger(__name__)

class TravelPlannerOrchestrator(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Lead Travel Orchestrator 🎓",
            role_description="You coordinate specialized sub-agents (Itinerary Planner, Budget & Discount Analyst, Safety Specialist) to craft seamless, budget-optimized student trips."
        )
        self.itinerary_agent = ItineraryAgent()
        self.budget_agent = BudgetAgent()
        self.packing_safety_agent = PackingSafetyAgent()

    def generate_full_trip_plan(
        self,
        destination: str,
        origin: str,
        duration: int,
        budget: float,
        currency_label: str = "USD ($)",
        travel_style: str = "Balanced",
        has_student_id: bool = True,
        interests: list = None,
        progress_callback = None
    ) -> dict:
        """
        Orchestrates all 3 agents to construct a comprehensive trip plan.
        Optional progress_callback for Streamlit UI status updates.
        """
        currency_symbol = CURRENCIES.get(currency_label, "$")
        interests = interests or []

        # Step 1: Budget & Discount Analysis
        if progress_callback:
            progress_callback("💸 **Budget & Discount Agent** calculating optimal allocations and student card hacks...")
        budget_res = self.budget_agent.analyze_budget_and_discounts(
            destination=destination,
            duration=duration,
            total_budget=budget,
            currency_symbol=currency_symbol,
            travel_style=travel_style
        )

        # Step 2: Itinerary Planning
        if progress_callback:
            progress_callback("🗺️ **Itinerary Planning Agent** crafting day-by-day student route...")
        itinerary_res = self.itinerary_agent.generate_itinerary(
            destination=destination,
            origin=origin,
            duration=duration,
            budget=budget,
            currency_symbol=currency_symbol,
            travel_style=travel_style,
            interests=interests
        )

        # Step 3: Packing & Safety Advice
        if progress_callback:
            progress_callback("🎒 **Safety & Packing Specialist** building checklist & safety guide...")
        safety_res = self.packing_safety_agent.generate_packing_and_safety(
            destination=destination,
            duration=duration,
            travel_style=travel_style
        )

        # Step 4: Executive Overview Synthesis
        if progress_callback:
            progress_callback("✨ **Lead Orchestrator** finalizing trip plan...")
        
        overview_text = self._synthesize_overview(destination, origin, duration, budget, currency_symbol, travel_style)

        full_plan = {
            "destination": destination,
            "origin": origin,
            "duration": duration,
            "budget": budget,
            "currency_label": currency_label,
            "currency_symbol": currency_symbol,
            "travel_style": travel_style,
            "has_student_id": has_student_id,
            "interests": interests,
            "overview": overview_text,
            "budget_breakdown": budget_res["budget_breakdown"],
            "discounts": budget_res["discounts_text"] + "\n\n" + budget_res["budget_advice"],
            "itinerary": itinerary_res,
            "packing_list": safety_res["packing_list"],
            "safety_advice": safety_res["safety_advice"]
        }

        return full_plan

    def _synthesize_overview(self, destination: str, origin: str, duration: int, budget: float, currency_symbol: str, travel_style: str) -> str:
        if self.has_active_client():
            prompt = f"Write a 2-paragraph inspiring overview for a {duration}-day student trip from {origin} to {destination} with a budget of {currency_symbol}{budget} ({travel_style}). Highlight why this trip is great for university students."
            try:
                return self.generate_response(prompt)
            except Exception as e:
                logger.warning(f"Overview synthesis fallback: {e}")

        return f"Welcome to your custom student travel blueprint for **{destination}**! Starting from **{origin}**, this {duration}-day itinerary is specially tailored for **{travel_style}** student travelers. With a total budget of **{currency_symbol}{budget}**, this plan maximizes student discounts, social hostel stays, cheap regional transit, and iconic sights without blowing your bank account."

    def chat_query(self, user_query: str, trip_context: dict = None) -> str:
        """
        Handles interactive conversational AI travel queries.
        """
        context_str = ""
        if trip_context:
            context_str = f"Current Trip Context: Destination: {trip_context.get('destination')}, Budget: {trip_context.get('currency_symbol')}{trip_context.get('budget')}, Duration: {trip_context.get('duration')} days."

        if self.has_active_client():
            prompt = f"{context_str}\nUser Question: {user_query}\nAnswer as an expert, friendly student travel advisor. Keep response helpful, concise, and formatted in markdown with clear bullet points."
            try:
                return self.generate_response(prompt)
            except Exception as e:
                logger.warning(f"Chat query fallback: {e}")

        # Fallback offline conversational logic
        query_lower = user_query.lower()
        if "budget" in query_lower or "cost" in query_lower or "money" in query_lower:
            return f"💡 **Student Budget Tip:** For {trip_context.get('destination', 'your trip') if trip_context else 'student trips'}, aim for hostel stays with free breakfast ({trip_context.get('currency_symbol', '$')}20-{trip_context.get('currency_symbol', '$')}40/night), buy a multi-day transit pass, and use student ID cards at attractions for 30%-100% off tickets."
        elif "hostel" in query_lower or "stay" in query_lower or "hotel" in query_lower:
            return f"🏨 **Hostel Recommendations:** Look on Hostelworld or Booking.com filtered by 'Rating 8.5+' and 'Guest Kitchen'. Top social student hostel chains in Europe/US include Hostel One, Generator, St Christopher's, and YHA."
        elif "food" in query_lower or "eat" in query_lower or "restaurant" in query_lower:
            return f"🍱 **Student Food Hacks:** Grab lunch deals at university cafeterias or bakeries, use the TooGoodToGo app for 60% off evening meals, and pick up fresh fruit and sandwiches from local supermarkets."
        else:
            return f"✈️ **Travel Advisor Answer:** For student trips to {trip_context.get('destination', 'your target destination') if trip_context else 'any destination'}, prioritize walkable routes, download offline maps (Maps.me / Google Maps offline), keep digital backups of your student ID, and book regional train tickets 2-4 weeks in advance for student tariffs."
