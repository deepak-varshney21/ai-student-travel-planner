"""
Packing & Safety Advice Agent
Generates weather & activity smart packing checklists and student safety guidelines.
"""

import logging
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class PackingSafetyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Safety & Packing Advisor 🎒",
            role_description="You are a seasoned student traveler safety expert. You provide weather-smart, minimalist packing checklists and crucial safety/scam warning advice for solo and group student travelers."
        )

    def generate_packing_and_safety(self, destination: str, duration: int, travel_style: str) -> dict:
        """
        Generates packing list items and safety tips.
        """
        ai_packing = []
        ai_safety = ""

        if self.has_active_client():
            prompt = f"""
Create a minimalist, smart student packing list and safety guide for a {duration}-day trip to {destination} ({travel_style}).

Return a JSON object with two keys:
1. "packing_list": list of string items (e.g. "Student ID card (ISIC)", "Universal travel adapter", "Compact microfiber towel")
2. "safety_tips": string formatted with markdown bullet points covering common tourist scams, emergency prep, hostel locker safety, and solo travel tips for students.
"""
            try:
                import json
                raw_response = self.generate_response(prompt)
                clean_json = raw_response.strip()
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].split("```")[0].strip()
                data = json.loads(clean_json)
                ai_packing = data.get("packing_list", [])
                ai_safety = data.get("safety_tips", "")
            except Exception as e:
                logger.warning(f"Fallback triggered for PackingSafetyAgent: {e}")

        if not ai_packing:
            ai_packing = self._generate_fallback_packing(destination, duration)
        if not ai_safety:
            ai_safety = self._generate_fallback_safety(destination)

        return {
            "packing_list": ai_packing,
            "safety_advice": ai_safety
        }

    def _generate_fallback_packing(self, destination: str, duration: int) -> list:
        return [
            "🎓 Valid Student ID / ISIC Card (Crucial for discounts!)",
            "🛂 Passport / Government ID + Digital & Physical Copies",
            "💳 Student Credit/Debit Card (Zero foreign transaction fees)",
            "🔌 Universal Travel Adapter + Power Bank (10,000mAh+)",
            "🔒 Padlock (Essential for hostel lockers)",
            "🚿 Quick-dry Microfiber Towel & Travel Toiletries",
            "👟 Comfortable Walking Shoes (Expect 15k+ steps/day)",
            "☔ Compact Rain Jacket / Windbreaker",
            "💊 Basic First Aid Kit (Pain relievers, Band-Aids, Motion sickness pills)",
            "🎧 Earplugs & Eye Mask (For dorm room sleeping)"
        ]

    def _generate_fallback_safety(self, destination: str) -> str:
        return f"""
### 🛡️ Essential Student Safety & Local Tips for {destination}:
- **Hostel Security:** Always use your own padlock on dorm lockers. Never leave electronics or passports unattended in common rooms.
- **Avoid Street Scams:** Beware of petition scams, unsolicited photo offers, or over-friendly strangers offering 'free' bracelets/flowers near major landmarks.
- **Night Safety:** Use official ride-hailing apps (Uber/Bolt) late at night rather than unregistered street taxis. Stick to well-lit student areas.
- **Digital Backup:** Store digital copies of your passport, visa, student ID, and travel insurance in cloud storage (Google Drive / iCloud).
- **Emergency Contact:** Save local emergency service numbers (112 in Europe, 911 in US) on your phone lock screen.
"""
