"""
Student Discount Finder & Database Tool
Provides specialized knowledge on student travel discounts, ISIC passes, railcard deals, and budget tips.
"""

STUDENT_DISCOUNT_DATABASE = [
    {
        "category": "Transit & Rail",
        "title": "Eurail / Interrail Youth Pass",
        "discount": "Up to 25% OFF for ages under 27",
        "description": "Flexible train travel across 33 European countries with student/youth discount pricing.",
        "regions": ["Europe", "EU", "France", "Germany", "Italy", "Spain", "Switzerland"]
    },
    {
        "category": "Transit & Rail",
        "title": "Amtrak Student Discount (USA)",
        "discount": "15% OFF for students aged 17-24",
        "description": "Valid on passenger rail travel across the US with valid student ID.",
        "regions": ["USA", "United States", "North America"]
    },
    {
        "category": "Transit & Rail",
        "title": "16-25 Railcard (UK)",
        "discount": "1/3 OFF train fares across Great Britain",
        "description": "Essential railcard for college students saving 34% on national train travel.",
        "regions": ["UK", "United Kingdom", "London", "Scotland"]
    },
    {
        "category": "Transit & Rail",
        "title": "Japan Rail Pass Youth Special",
        "discount": "Regional pass discounts for students",
        "description": "Save on Shinkansen bullet trains with JR regional passes.",
        "regions": ["Japan", "Tokyo", "Kyoto", "Asia"]
    },
    {
        "category": "Flights",
        "title": "StudentUniverse & Faremaker",
        "discount": "Exclusive student airfares (10%-30% lower)",
        "description": "Special flight tariffs with extra baggage allowance for verified college students.",
        "regions": ["Global", "Worldwide", "USA", "Europe", "Asia"]
    },
    {
        "category": "Flights",
        "title": "Emirates & Qatar Airways Student Club",
        "discount": "10% discount + 10kg extra baggage + free Wi-Fi",
        "description": "Free loyalty club for international students studying abroad.",
        "regions": ["Global", "Worldwide", "Europe", "Asia", "Middle East"]
    },
    {
        "category": "Accommodation",
        "title": "Hostelworld & YHA / HI Hostels",
        "discount": "10%-15% OFF with ISIC card",
        "description": "Budget hostel networks offering clean, social student dorms with free breakfast.",
        "regions": ["Global", "Worldwide", "Europe", "Asia", "Americas"]
    },
    {
        "category": "Attractions & Museums",
        "title": "Free EU Museum Entry for EU Students < 26",
        "discount": "100% FREE Entry",
        "description": "Louvre, Musée d'Orsay, Colosseum, Uffizi Gallery are free for EU residents under 26.",
        "regions": ["Europe", "France", "Paris", "Italy", "Rome", "Florence"]
    },
    {
        "category": "Attractions & Museums",
        "title": "ISIC (International Student Identity Card)",
        "discount": "150,000+ global student discounts",
        "description": "The only globally recognized proof of full-time student status for museum & transport entry.",
        "regions": ["Global", "Worldwide"]
    },
    {
        "category": "Food & Dining",
        "title": "Too Good To Go App",
        "discount": "50%-70% OFF fresh restaurant food",
        "description": "Surplus food bags from bakeries, cafes, and supermarkets at end-of-day prices.",
        "regions": ["Europe", "USA", "UK"]
    },
    {
        "category": "Connectivity",
        "title": "Airalo / Holafly Student e-SIM",
        "discount": "10%-15% OFF data plans",
        "description": "Cheap local data eSIMs to avoid international roaming charges.",
        "regions": ["Global", "Worldwide"]
    }
]

def search_discounts(destination: str = "", category: str = "") -> list:
    """Filter discounts based on destination region or category."""
    results = []
    dest_lower = destination.lower().strip()
    cat_lower = category.lower().strip()
    
    for item in STUDENT_DISCOUNT_DATABASE:
        matches_dest = False
        if not dest_lower:
            matches_dest = True
        else:
            for region in item["regions"]:
                if region.lower() in dest_lower or dest_lower in region.lower() or region.lower() == "global" or region.lower() == "worldwide":
                    matches_dest = True
                    break
                    
        matches_cat = False
        if not cat_lower or cat_lower in item["category"].lower():
            matches_cat = True
            
        if matches_dest and matches_cat:
            results.append(item)
            
    return results

def get_discount_summary_text(destination: str) -> str:
    """Format matching discounts into a clean summary text."""
    discounts = search_discounts(destination)
    if not discounts:
        discounts = STUDENT_DISCOUNT_DATABASE[:4]  # Return default global discounts
        
    lines = []
    for d in discounts:
        lines.append(f"• **{d['title']}** [{d['category']}]: {d['discount']} - {d['description']}")
    return "\n".join(lines)
