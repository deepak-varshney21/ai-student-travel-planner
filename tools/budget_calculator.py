"""
Budget Calculation & Optimization Tool
Performs financial calculations, budget allocations, and generates visualization charts for student trips.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def calculate_budget_breakdown(total_budget: float, num_days: int, travel_style: str = "Balanced"):
    """
    Calculates estimated budget allocations based on travel style.
    Returns dictionary with breakdown figures and daily allowances.
    """
    num_days = max(1, num_days)
    
    # Ratios depending on travel style
    if "Backpacker" in travel_style:
        ratios = {"Accommodation": 0.35, "Transport": 0.20, "Food & Drinks": 0.25, "Sightseeing & Pass": 0.12, "Emergency Fund": 0.08}
    elif "Comfort" in travel_style:
        ratios = {"Accommodation": 0.45, "Transport": 0.15, "Food & Drinks": 0.25, "Sightseeing & Pass": 0.10, "Emergency Fund": 0.05}
    else:  # Balanced
        ratios = {"Accommodation": 0.40, "Transport": 0.18, "Food & Drinks": 0.25, "Sightseeing & Pass": 0.10, "Emergency Fund": 0.07}
        
    breakdown = {}
    for cat, weight in ratios.items():
        breakdown[cat] = round(total_budget * weight, 2)
        
    daily_spendable = round((total_budget - breakdown["Emergency Fund"]) / num_days, 2)
    daily_food = round(breakdown["Food & Drinks"] / num_days, 2)
    daily_hostel = round(breakdown["Accommodation"] / num_days, 2)
    
    return {
        "total_budget": total_budget,
        "num_days": num_days,
        "breakdown": breakdown,
        "daily_total_allowance": daily_spendable,
        "daily_food_target": daily_food,
        "daily_hostel_target": daily_hostel,
        "estimated_student_savings": round(total_budget * 0.18, 2)  # ~18% savings with student discounts
    }

def create_budget_pie_chart(breakdown_dict: dict, currency_symbol: str = "$"):
    """Generates a Plotly pie chart for budget categories."""
    df = pd.DataFrame([
        {"Category": cat, "Amount": amt}
        for cat, amt in breakdown_dict.items()
    ])
    
    fig = px.pie(
        df,
        names="Category",
        values="Amount",
        title="<b>Student Travel Budget Breakdown</b>",
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        hole=0.4
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Amount: " + currency_symbol + "%{value:,.2f}<br>(%{percent})"
    )
    
    fig.update_layout(
        margin=dict(t=50, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_savings_comparison_bar(total_budget: float, student_savings: float, currency_symbol: str = "$"):
    """Generates a bar chart comparing Standard Trip vs Student Saver Trip."""
    standard_cost = total_budget + student_savings
    df = pd.DataFrame([
        {"Type": "Standard Adult Rate", "Cost": standard_cost, "Color": "#EF553B"},
        {"Type": "Student Discount Rate", "Cost": total_budget, "Color": "#00CC96"}
    ])
    
    fig = px.bar(
        df,
        x="Type",
        y="Cost",
        text="Cost",
        title="<b>Standard vs Student Pass Savings</b>",
        color="Type",
        color_discrete_map={"Standard Adult Rate": "#EF553B", "Student Discount Rate": "#00CC96"}
    )
    
    fig.update_traces(
        texttemplate=currency_symbol + "%{text:,.2f}",
        textposition='outside'
    )
    
    fig.update_layout(
        showlegend=False,
        yaxis_title=f"Total Cost ({currency_symbol})",
        margin=dict(t=50, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig
