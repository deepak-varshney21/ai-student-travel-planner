"""
Budget & Discount Management Agent
Analyzes student travel budgets, identifies student discounts, and suggests budget saving hacks.
"""

import logging
from agents.base_agent import BaseAgent
from tools.budget_calculator import calculate_budget_breakdown
from tools.discount_db import get_discount_summary_text

logger = logging.getLogger(__name__)

class BudgetAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Budget & Discount Agent 💸",
            role_description="You are a financial advisor specialized in student travel. You find maximum student discounts (ISIC, rail cards, student flights, hostel hacks) and optimize trip budgets to prevent overspending."
        )

    def analyze_budget_and_discounts(self, destination: str, duration: int, total_budget: float, currency_symbol: str, travel_style: str) -> dict:
        """
        Calculates mathematical budget breakdown and generates tailored discount recommendations.
        """
        breakdown_data = calculate_budget_breakdown(total_budget, duration, travel_style)
        discount_text = get_discount_summary_text(destination)

        ai_advice = ""
        if self.has_active_client():
            prompt = f"""
Provide top 4 student budget hacks and discount strategies for traveling to {destination} on a budget of {currency_symbol}{total_budget} for {duration} days ({travel_style}).
Mention specific passes (e.g. transit pass, hostel membership, museum pass, meal deals). Keep it concise, energetic, and highly practical for college students.
"""
            try:
                ai_advice = self.generate_response(prompt)
            except Exception as e:
                logger.warning(f"Fallback triggered for BudgetAgent AI advice: {e}")

        if not ai_advice:
            ai_advice = self._generate_fallback_advice(destination, total_budget, currency_symbol, travel_style)

        return {
            "budget_breakdown": breakdown_data,
            "discounts_text": discount_text,
            "budget_advice": ai_advice
        }

    def _generate_fallback_advice(self, destination: str, budget: float, currency: str, style: str) -> str:
        return f"""
### 💡 Top Student Budget Hacks for {destination}:
1. **Get an ISIC / Student Card:** Carry your university ID or ISIC card everywhere. Most top museums, galleries, and historic sites offer 30% to 100% off for verified students.
2. **Book Hostels with Free Breakfast:** Save {currency}8-{currency}15 daily by picking social hostels with kitchen facilities and complimentary breakfast.
3. **Use Transit Multi-Day Passes:** Avoid single-ride transport tickets. Purchase 3-day or 7-day student transit cards or bike rentals.
4. **Eat Like a Local Student:** Look for university cafeterias, bakeries late-day discounts (or TooGoodToGo app), and street food stalls near university campuses.
"""
