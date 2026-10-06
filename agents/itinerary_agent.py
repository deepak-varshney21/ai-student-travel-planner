"""
Itinerary Planning Agent
Generates student-friendly day-by-day travel itineraries.
"""

import json
import logging
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ItineraryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Itinerary Planning Agent 🗺️",
            role_description="You specialize in creating exciting, budget-conscious, day-by-day student travel itineraries. You prioritize walkable routes, free museum days, budget food, student night spots, and public transport."
        )

    def generate_itinerary(self, destination: str, origin: str, duration: int, budget: float, currency_symbol: str, travel_style: str, interests: list) -> list:
        """
        Generates a day-by-day itinerary list.
        """
        prompt = f"""
Create a detailed {duration}-day student travel itinerary for visiting {destination} from {origin}.
Total Budget: {currency_symbol}{budget} for {duration} days.
Travel Style: {travel_style}
Special Interests: {', '.join(interests) if interests else 'General sightseeing'}

Return a JSON array of objects, where each object represents one day with the following keys:
- "day": integer (1, 2, ...)
- "title": short theme for the day (e.g., "Historic Core & Free Walking Tour")
- "morning": detailed activity description for morning
- "afternoon": detailed activity description for afternoon
- "evening": detailed activity description for evening
- "estimated_cost": estimated daily expense number (without symbol)
- "budget_tip": specific student money-saving tip for this day (e.g. use student pass, buy lunch deal)
- "transport": recommended cheap transport mode (e.g. metro pass, walking, bike rental)
"""
        if self.has_active_client():
            try:
                raw_response = self.generate_response(prompt)
                # Attempt to extract JSON from response string
                clean_json = raw_response.strip()
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].split("```")[0].strip()
                return json.loads(clean_json)
            except Exception as e:
                logger.warning(f"Fallback triggered for ItineraryAgent due to: {e}")

        # Smart fallback itinerary generator
        return self._generate_fallback_itinerary(destination, origin, duration, budget, currency_symbol, travel_style, interests)

    def _generate_fallback_itinerary(self, destination: str, origin: str, duration: int, budget: float, currency_symbol: str, travel_style: str, interests: list) -> list:
        daily_est = round(budget / max(1, duration), 2)
        itinerary = []
        
        activities_pool = [
            ("Historic Center & Walking Tour", 
             f"Join a free student walking tour through central {destination} starting at the main square. Visit historical landmarks.",
             "Picnic lunch from a local market. Explore popular public gardens and historic monuments with free student entry.",
             "Visit a vibrant student street food market or budget hostel bar for local social networking.",
             f"Show your student ID at museums to get 50%-100% off tickets.",
             "Walking & Metro"),
            
            ("Art, Museums & Culture",
             "Visit the premier national museum or art gallery (free with student ID or ISIC card).",
             "Explore bohemian art districts, local street art alleys, and indie bookshops.",
             "Budget dinner at a university-area eatery. Enjoy sunset views from a free city elevation viewpoint.",
             "Many galleries have free entry after 3 PM on weekdays for students.",
             "City Bus / Tram"),
            
            ("Local Markets & Hidden Gems",
             "Morning stroll through local flea markets and artisan craft stalls. Grab budget pastries/coffee.",
             "Rent a city bicycle or walk to a nearby waterfront / lake / park district for relaxation.",
             "Attend a live student music venue, comedy night, or hostel social event.",
             "Buy snacks and drinks from supermarkets instead of tourist cafes.",
             "Bike Share / Metro"),

            ("Day Trip & Scenic Nature",
             "Take early morning local commuter train/bus to a picturesque nearby town or natural viewpoint.",
             "Hike scenic trails or explore local coastlines/parks. Enjoy packed lunch.",
             "Return to main city center. Try authentic local street food dishes (e.g., kebabs, tapas, ramen).",
             "Buy regional day transit passes for unlimited group travel discounts.",
             "Regional Commuter Train"),

            ("Student Nightlife & Departure Prep",
             "Visit local student cafes and university neighborhood campuses.",
             "Souvenir shopping at local student markets; capture final photos at iconic photo spots.",
             "Farewell student hostel dinner and rooftop gathering with fellow travelers.",
             "Check student discounts on luggage storage and airport shuttle buses.",
             "Metro / Airport Express Bus")
        ]
        
        for d in range(1, duration + 1):
            pool_idx = (d - 1) % len(activities_pool)
            title, morning, afternoon, evening, tip, transport = activities_pool[pool_idx]
            itinerary.append({
                "day": d,
                "title": f"Day {d}: {title}",
                "morning": morning,
                "afternoon": afternoon,
                "evening": evening,
                "estimated_cost": daily_est,
                "budget_tip": tip,
                "transport": transport
            })
            
        return itinerary
