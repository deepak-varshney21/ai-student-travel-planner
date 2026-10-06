"""
Student Travel Planner Agent System
Streamlit Web Application
"""

import os
import time
import json
import streamlit as st
import pandas as pd

from config import APP_TITLE, APP_TAGLINE, TRAVEL_STYLES, CURRENCIES, GEMINI_API_KEY
from agents.orchestrator import TravelPlannerOrchestrator
from tools.budget_calculator import create_budget_pie_chart, create_savings_comparison_bar
from tools.discount_db import STUDENT_DISCOUNT_DATABASE, search_discounts
from tools.exporter import generate_markdown_export, generate_html_export

# Page Setup
st.set_page_config(
    page_title="Student Travel Planner AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
css_path = os.path.join("assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Session States
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = TravelPlannerOrchestrator()
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Hi there! I'm your AI Student Travel Advisor. Ask me anything about student budgets, hostel picks, rail passes, or trip safety!"}
    ]
if "packing_states" not in st.session_state:
    st.session_state.packing_states = {}

# --- SIDEBAR & CONFIGURATION ---
st.sidebar.markdown("## 🎓 Agent Configuration")

# API Key Handling
api_key_input = st.sidebar.text_input(
    "Google Gemini API Key (Optional)",
    value=os.environ.get("GEMINI_API_KEY", ""),
    type="password",
    help="Leave blank to use intelligent offline/demo mode or add your GEMINI_API_KEY for live Gemini 2.5 Flash responses."
)

if api_key_input:
    os.environ["GEMINI_API_KEY"] = api_key_input
    st.session_state.orchestrator = TravelPlannerOrchestrator()
    st.sidebar.success("🟢 Gemini API Key Active")
else:
    st.sidebar.info("🟡 Running in Smart Offline/Demo Mode")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Active Agent Team")
st.sidebar.markdown("• **Lead Orchestrator Agent** (Synthesis & Chat)\n"
                   "• **Itinerary Agent 🗺️** (Routes & Schedules)\n"
                   "• **Budget Agent 💸** (Math & Discounts)\n"
                   "• **Safety Advisor 🎒** (Checklists & Tips)")

st.sidebar.markdown("---")
st.sidebar.markdown("### ✈️ Trip Input Parameters")

destination = st.sidebar.text_input("Destination City/Country", value="Paris, France")
origin = st.sidebar.text_input("Starting Location", value="London, UK")
duration = st.sidebar.slider("Trip Duration (Days)", min_value=1, max_value=14, value=4)
currency_label = st.sidebar.selectbox("Currency", list(CURRENCIES.keys()), index=0)
budget = st.sidebar.number_input(f"Total Budget ({CURRENCIES[currency_label]})", min_value=50, max_value=10000, value=450, step=50)

travel_style = st.sidebar.selectbox("Student Travel Style", TRAVEL_STYLES, index=1)
has_student_id = st.sidebar.checkbox("I have a valid Student ID / ISIC card", value=True)

interests = st.sidebar.multiselect(
    "Special Interests",
    ["🏛️ Art & Museums", "🍕 Foodie & Street Food", "🎉 Nightlife & Bars", "🏔️ Nature & Hiking", "🛍️ Thrift Shopping", "📸 Photography", "🏛️ History"],
    default=["🏛️ Art & Museums", "🍕 Foodie & Street Food"]
)

# --- HEADER SECTION ---
st.markdown(f"<div class='main-header'>{APP_TITLE}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-header'>{APP_TAGLINE}</div>", unsafe_allow_html=True)

# --- MAIN TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ AI Trip Planner",
    "💸 Student Discount Explorer",
    "💬 AI Travel Advisor Chat",
    "📄 Export & Save Plan"
])

# ==========================================
# TAB 1: AI TRIP PLANNER
# ==========================================
with tab1:
    col_input, col_action = st.columns([3, 1])
    with col_input:
        st.markdown(f"**Target:** {origin} ➔ **{destination}** | **Duration:** {duration} Days | **Budget:** {CURRENCIES[currency_label]}{budget:,} ({travel_style})")
    with col_action:
        generate_btn = st.button("⚡ Generate Plan with Agents", use_container_width=True)

    if generate_btn:
        progress_box = st.empty()

        def update_progress(msg):
            progress_box.info(msg)
            time.sleep(0.4)

        with st.spinner("Multi-Agent system is working..."):
            plan = st.session_state.orchestrator.generate_full_trip_plan(
                destination=destination,
                origin=origin,
                duration=duration,
                budget=budget,
                currency_label=currency_label,
                travel_style=travel_style,
                has_student_id=has_student_id,
                interests=interests,
                progress_callback=update_progress
            )
            st.session_state.current_plan = plan
            st.session_state.packing_states = {item: False for item in plan.get("packing_list", [])}
            progress_box.success("✨ Multi-Agent Travel Plan Generated Successfully!")

    # Display Current Trip Plan
    if st.session_state.current_plan:
        plan = st.session_state.current_plan
        curr_sym = plan.get("currency_symbol", "$")

        st.markdown("---")
        st.markdown(f"### 🌟 Trip Overview: {plan['destination']}")
        st.write(plan["overview"])

        # Key Metrics Row
        b_data = plan.get("budget_breakdown", {})
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Budget", f"{curr_sym}{plan['budget']:,}")
        with m2:
            st.metric("Daily Spend Target", f"{curr_sym}{b_data.get('daily_total_allowance', 0):,.2f}")
        with m3:
            st.metric("Hostel Daily Target", f"{curr_sym}{b_data.get('daily_hostel_target', 0):,.2f}")
        with m4:
            st.metric("Estimated Student Savings", f"{curr_sym}{b_data.get('estimated_student_savings', 0):,.2f}", delta="Saved with Student ID")

        st.markdown("---")

        # Layout: Left = Itinerary, Right = Budget & Packing
        col_left, col_right = st.columns([3, 2])

        with col_left:
            st.markdown("### 🗓️ Day-by-Day Student Itinerary")
            itinerary = plan.get("itinerary", [])
            for day_item in itinerary:
                day_num = day_item.get("day", 1)
                day_title = day_item.get("title", f"Day {day_num}")
                
                with st.expander(f"📌 **{day_title}** (Est: {curr_sym}{day_item.get('estimated_cost', 0)})", expanded=(day_num == 1)):
                    st.markdown(f"🌅 **Morning:** {day_item.get('morning', 'N/A')}")
                    st.markdown(f"☀️ **Afternoon:** {day_item.get('afternoon', 'N/A')}")
                    st.markdown(f"🌙 **Evening:** {day_item.get('evening', 'N/A')}")
                    st.markdown(f"💡 **Student Tip:** {day_item.get('budget_tip', 'N/A')}")
                    st.markdown(f"🚌 **Transport:** `{day_item.get('transport', 'Walk')}`")

        with col_right:
            st.markdown("### 📊 Budget Breakdown & Savings")
            if "breakdown" in b_data:
                fig_pie = create_budget_pie_chart(b_data["breakdown"], curr_sym)
                st.plotly_chart(fig_pie, use_container_width=True)

                fig_bar = create_savings_comparison_bar(plan["budget"], b_data.get("estimated_student_savings", 0), curr_sym)
                st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("### 🏷️ Student Discounts & Passes")
            st.info(plan.get("discounts", "No specific discounts found."))

            st.markdown("### 🎒 Student Packing Checklist")
            packing_items = plan.get("packing_list", [])
            for item in packing_items:
                st.checkbox(item, key=f"pack_{item}")

            st.markdown("### 🛡️ Safety & Local Tips")
            st.warning(plan.get("safety_advice", "Stay alert in crowded tourist spots."))
    else:
        st.info("👈 Set your travel preferences in the sidebar and click **'⚡ Generate Plan with Agents'** to create your customized student trip blueprint!")


# ==========================================
# TAB 2: STUDENT DISCOUNT EXPLORER
# ==========================================
with tab2:
    st.markdown("### 🏷️ Global Student Discount & Travel Pass Finder")
    st.write("Browse verified student discounts, railcards, hostel perks, and cheap flight benefits worldwide.")

    c1, c2 = st.columns(2)
    with c1:
        search_region = st.text_input("Filter by Region / Destination", value="")
    with c2:
        search_cat = st.selectbox("Filter by Category", ["All Categories", "Transit & Rail", "Flights", "Accommodation", "Attractions & Museums", "Food & Dining", "Connectivity"])

    cat_query = "" if search_cat == "All Categories" else search_cat
    discount_results = search_discounts(destination=search_region, category=cat_query)

    st.markdown(f"Found **{len(discount_results)}** student discount passes & deals:")
    
    for item in discount_results:
        with st.container():
            st.markdown(f"#### 🎫 {item['title']} <span style='font-size:0.8em; color:#3182CE; background:#EBF8FF; padding:2px 8px; border-radius:4px;'>{item['category']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Discount:** `{item['discount']}`")
            st.write(item['description'])
            st.caption(f"Valid Regions: {', '.join(item['regions'])}")
            st.markdown("---")


# ==========================================
# TAB 3: AI TRAVEL ADVISOR CHAT
# ==========================================
with tab3:
    st.markdown("### 💬 AI Student Travel Advisor")
    st.write("Ask questions about your planned trip, budget calculations, hostel safety, transport pass options, or local student spots!")

    # Quick starter buttons
    st.markdown("**Quick Questions:**")
    q_cols = st.columns(3)
    preset_query = None
    if q_cols[0].button("💡 How to cut food costs?"):
        preset_query = "What are the best hacks for cutting food costs while traveling as a student?"
    if q_cols[1].button("🚆 Should I buy a Rail Pass?"):
        preset_query = f"Is a rail pass worth it for a trip to {destination}?"
    if q_cols[2].button("🏨 How to pick safe hostels?"):
        preset_query = "What should I look for when choosing safe, social budget hostels?"

    # Render Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle User Input
    user_input = st.chat_input("Ask a travel question...") or preset_query

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_text = st.session_state.orchestrator.chat_query(
                    user_query=user_input,
                    trip_context=st.session_state.current_plan
                )
                st.markdown(response_text)
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})


# ==========================================
# TAB 4: EXPORT & SAVE PLAN
# ==========================================
with tab4:
    st.markdown("### 📄 Export & Download Your Travel Blueprint")
    if st.session_state.current_plan:
        plan = st.session_state.current_plan
        md_text = generate_markdown_export(plan)
        html_text = generate_html_export(plan)

        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button(
                label="📥 Download Itinerary (Markdown .md)",
                data=md_text,
                file_name=f"student_trip_{plan['destination'].lower().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_exp2:
            st.download_button(
                label="🌐 Download Printable Itinerary (HTML)",
                data=html_text,
                file_name=f"student_trip_{plan['destination'].lower().replace(' ', '_')}.html",
                mime="text/html",
                use_container_width=True
            )

        st.markdown("---")
        st.markdown("#### 📝 Markdown Preview")
        st.code(md_text, language="markdown")
    else:
        st.info("No active trip plan generated yet. Generate a plan in the '🗺️ AI Trip Planner' tab first!")
