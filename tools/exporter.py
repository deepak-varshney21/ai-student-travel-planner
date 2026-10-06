"""
Export & Formatting Utility Tool
Exports travel itineraries into Markdown and HTML printable format.
"""

def generate_markdown_export(plan_data: dict) -> str:
    """Formats full trip plan dictionary into Markdown."""
    destination = plan_data.get("destination", "Destination")
    origin = plan_data.get("origin", "Home")
    duration = plan_data.get("duration", "N/A")
    budget = plan_data.get("budget", "N/A")
    currency = plan_data.get("currency_symbol", "$")
    
    md = []
    md.append(f"# 🎓 Student Travel Plan: {destination}")
    md.append(f"**From:** {origin} | **Duration:** {duration} Days | **Total Budget:** {currency}{budget}")
    md.append(f"**Travel Style:** {plan_data.get('travel_style', 'Balanced')} | **Student ID Applied:** Yes\n")
    md.append("---")
    
    # Executive Summary / Overview
    if "overview" in plan_data:
        md.append("## 🌟 Trip Highlights & Overview")
        md.append(plan_data["overview"])
        md.append("")
        
    # Budget Breakdown
    if "budget_breakdown" in plan_data:
        b = plan_data["budget_breakdown"]
        md.append("## 💸 Budget Breakdown")
        for cat, amt in b.get("breakdown", {}).items():
            md.append(f"- **{cat}:** {currency}{amt:,.2f}")
        md.append(f"\n💡 *Estimated Student ID Savings:* **{currency}{b.get('estimated_student_savings', 0):,.2f}**")
        md.append(f"🎯 *Daily Spendable Target:* **{currency}{b.get('daily_total_allowance', 0):,.2f}/day**\n")
        
    # Student Discounts
    if "discounts" in plan_data:
        md.append("## 🏷️ Recommended Student Discounts & Passes")
        md.append(plan_data["discounts"])
        md.append("")
        
    # Daily Itinerary
    if "itinerary" in plan_data:
        md.append("## 🗓️ Day-by-Day Itinerary")
        if isinstance(plan_data["itinerary"], list):
            for day in plan_data["itinerary"]:
                md.append(f"### Day {day.get('day', 1)}: {day.get('title', 'Exploration')}")
                if "morning" in day:
                    md.append(f"- **Morning:** {day['morning']}")
                if "afternoon" in day:
                    md.append(f"- **Afternoon:** {day['afternoon']}")
                if "evening" in day:
                    md.append(f"- **Evening:** {day['evening']}")
                if "budget_tip" in day:
                    md.append(f"- 💡 *Student Budget Tip:* {day['budget_tip']}")
                md.append("")
        else:
            md.append(str(plan_data["itinerary"]))
            md.append("")
            
    # Packing List
    if "packing_list" in plan_data:
        md.append("## 🎒 Student Packing Checklist")
        if isinstance(plan_data["packing_list"], list):
            for item in plan_data["packing_list"]:
                md.append(f"- [ ] {item}")
        else:
            md.append(str(plan_data["packing_list"]))
        md.append("")
        
    # Safety Advice
    if "safety_advice" in plan_data:
        md.append("## 🛡️ Safety & Local Tips")
        md.append(plan_data["safety_advice"])
        md.append("")
        
    md.append("---\n*Generated with Student Travel Planner AI Agent System*")
    return "\n".join(md)

def generate_html_export(plan_data: dict) -> str:
    """Formats full trip plan into a printable styled HTML page."""
    md_content = generate_markdown_export(plan_data)
    # Simple markdown-to-html transformation with CSS styling
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Student Travel Plan - {plan_data.get('destination', 'Trip')}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #2D3748; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2B6CB0; border-bottom: 2px solid #63B3ED; padding-bottom: 8px; }}
        h2 {{ color: #2C5282; margin-top: 25px; border-bottom: 1px solid #E2E8F0; padding-bottom: 5px; }}
        h3 {{ color: #3182CE; }}
        ul {{ list-style-type: none; padding-left: 0; }}
        li {{ margin-bottom: 8px; padding: 6px 12px; background: #F7FAFC; border-left: 4px solid #4299E1; border-radius: 2px; }}
        .badge {{ background: #EBF8FF; color: #2B6CB0; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
    </style>
</head>
<body>
    <pre style="white-space: pre-wrap; font-family: inherit;">{md_content}</pre>
</body>
</html>"""
    return html
