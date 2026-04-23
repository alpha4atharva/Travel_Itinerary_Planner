"""
tasks.py — Defines the Tasks assigned to each CrewAI Agent.

Tasks:
    1. Research Task       — Explore the destination for activities & dining.
    2. Logistics Task      — Find flight/hotel costs and verify budget.
    3. Compilation Task    — Build the final day-by-day itinerary.
"""

from crewai import Task
from backend.agents import (
    create_travel_researcher,
    create_logistics_manager,
    create_itinerary_compiler,
)


def create_research_task(researcher) -> Task:
    """Task for the Travel Researcher agent.

    Searches the web for top attractions, restaurants, and local tips
    at the user's chosen destination.
    """
    return Task(
        description=(
            "Search the web and compile a comprehensive travel guide for {destination}.\n\n"
            "Your research must include:\n"
            "1. Top 5-7 must-visit attractions or landmarks.\n"
            "2. 3-5 highly-rated restaurants or food experiences (with cuisine type).\n"
            "3. Local customs or travel tips (e.g., tipping culture, transport, safety).\n"
            "4. Current weather/season conditions for the travel dates.\n"
            "5. Any free or budget-friendly activities available.\n\n"
            "Focus on making the recommendations practical and actionable."
        ),
        expected_output=(
            "A structured research report in markdown format with sections for:\n"
            "- **Top Attractions** (name, brief description, estimated entry cost)\n"
            "- **Dining Recommendations** (name, cuisine, price range)\n"
            "- **Local Tips** (transport, customs, safety)\n"
            "- **Weather & Best Time to Visit**\n"
            "- **Budget-Friendly Activities**"
        ),
        agent=researcher,
    )


def create_logistics_task(logistics_manager) -> Task:
    """Task for the Logistics & Budget Manager agent.

    Finds estimated flight and hotel costs, then verifies the total
    fits within the user's budget.
    """
    return Task(
        description=(
            "Find realistic cost estimates for a trip from {origin} to {destination} "
            "for {num_days} days.\n\n"
            "You must research and provide:\n"
            "1. **Flights:** Average round-trip flight cost from {origin} to {destination}.\n"
            "2. **Hotels:** Average nightly hotel rate in {destination} "
            "(search for mid-range options).\n"
            "3. **Daily Expenses:** Estimated daily food and local transport costs.\n"
            "4. **Total Cost Calculation:**\n"
            "   - Flights (round-trip)\n"
            "   - Hotel ({num_days} nights × nightly rate)\n"
            "   - Daily expenses ({num_days} days × daily cost)\n"
            "   - TOTAL\n\n"
            "5. **Budget Check:** Compare the total against the budget of ₹{budget}.\n"
            "   - If over budget, suggest specific ways to cut costs.\n"
            "   - If under budget, mention how much is left for shopping/extras."
        ),
        expected_output=(
            "A detailed cost breakdown in markdown format:\n"
            "- **Flight Estimate:** ₹XXX (round-trip)\n"
            "- **Hotel Estimate:** ₹XXX/night × {num_days} nights = ₹XXX\n"
            "- **Daily Expenses:** ₹XXX/day × {num_days} days = ₹XXX\n"
            "- **TOTAL ESTIMATED COST:** ₹XXX\n"
            "- **Budget Remaining:** ₹XXX\n"
            "- **Budget Status:** ✅ Within Budget / ⚠️ Over Budget\n"
            "- **Suggestions** (if over budget)"
        ),
        agent=logistics_manager,
    )


def create_compilation_task(compiler, context_tasks: list) -> Task:
    """Task for the Itinerary Compiler agent.

    Takes the outputs of the research and logistics tasks and compiles
    a polished, day-by-day travel itinerary.
    """
    return Task(
        description=(
            "Using the research report and the cost breakdown provided by your "
            "teammates, create a detailed day-by-day travel itinerary for "
            "{num_days} days in {destination}.\n\n"
            "The itinerary must:\n"
            "1. Start with a **Trip Summary** (destination, dates, total cost, budget status).\n"
            "2. Include a **Cost Breakdown** table.\n"
            "3. Have a section for each day (Day 1, Day 2, etc.) with:\n"
            "   - Morning, Afternoon, and Evening activities.\n"
            "   - Restaurant/food suggestions for each meal.\n"
            "   - Estimated costs for each activity.\n"
            "4. End with **Packing Tips** and **Important Notes**.\n\n"
            "Format the entire output as clean, well-structured Markdown."
        ),
        expected_output=(
            "A complete, beautifully formatted Markdown travel itinerary with:\n"
            "- Trip Summary header\n"
            "- Cost Breakdown table\n"
            "- Day-by-day schedule (Day 1 through Day {num_days})\n"
            "- Each day has Morning / Afternoon / Evening sections\n"
            "- Packing Tips section\n"
            "- Important Notes section"
        ),
        agent=compiler,
        context=context_tasks,  # This agent reads the outputs of the previous tasks.
    )
