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
            "The traveler is interested in: {interests}.\n"
            "Tailor your recommendations to match these interests.\n\n"
            "Your research must include:\n"
            "1. Top 5-7 must-visit attractions or landmarks that match the traveler's interests.\n"
            "2. 3-5 highly-rated restaurants or food experiences (with cuisine type).\n"
            "3. Local customs or travel tips (e.g., tipping culture, transport, safety).\n"
            "4. Current weather/season conditions for the travel dates starting on {start_date}.\n"
            "5. Any free or budget-friendly activities available.\n\n"
            "Focus on making the recommendations practical and actionable."
        ),
        expected_output=(
            "A structured research report in markdown format with sections for:\n"
            "- **Top Attractions** (name, brief description, estimated entry cost in {currency_symbol})\n"
            "- **Dining Recommendations** (name, cuisine, price range in {currency_symbol})\n"
            "- **Local Tips** (transport, customs, safety)\n"
            "- **Weather & Best Time to Visit**\n"
            "- **Budget-Friendly Activities**"
        ),
        agent=researcher,
        async_execution=True,  # Run in parallel with logistics task
    )


def create_logistics_task(logistics_manager) -> Task:
    """Task for the Logistics & Budget Manager agent.

    Finds estimated flight and hotel costs, then verifies the total
    fits within the user's budget.
    """
    return Task(
        description=(
            "Find realistic and SPECIFIC cost estimates for a trip from {origin} to {destination} "
            "starting on {start_date} for {num_days} days.\n\n"
            "All prices must be in {currency} ({currency_symbol}).\n\n"
            "You must research and provide:\n"
            "1. **Travel (Flights/Trains/Buses):** Find real travel options from {origin} to {destination}. "
            "You MUST provide the specific Airline/Train name and the estimated price. "
            "Do NOT just say 'train travel' or 'average flight'. Provide specific names.\n"
            "2. **Accommodation:** Find 2-3 specific hotels or guesthouses in {destination} that fit the budget. "
            "You MUST provide the ACTUAL NAME of the hotel and its nightly rate. "
            "Do NOT just say 'budget guesthouse'.\n"
            "3. **Daily Expenses:** Estimated daily food and local transport costs.\n"
            "4. **Total Cost Calculation:**\n"
            "   - Travel costs\n"
            "   - Hotel ({num_days} nights × nightly rate)\n"
            "   - Daily expenses ({num_days} days × daily cost)\n"
            "   - TOTAL\n\n"
            "5. **Budget Check:** Compare the total against the budget of {currency_symbol}{budget}.\n"
            "   - If over budget, suggest specific ways to cut costs."
        ),
        expected_output=(
            "A detailed cost breakdown in markdown format:\n"
            "- **Travel Options:** [Specific Airline/Train Name] - {currency_symbol}XXX\n"
            "- **Recommended Hotel:** [Specific Hotel Name] - {currency_symbol}XXX/night × {num_days} nights = {currency_symbol}XXX\n"
            "- **Daily Expenses:** {currency_symbol}XXX/day × {num_days} days = {currency_symbol}XXX\n"
            "- **TOTAL ESTIMATED COST:** {currency_symbol}XXX\n"
            "- **Budget Remaining:** {currency_symbol}XXX\n"
            "- **Budget Status:** ✅ Within Budget / ⚠️ Over Budget"
        ),
        agent=logistics_manager,
        async_execution=True,  # Run in parallel with research task
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
            "{num_days} days in {destination}, starting on {start_date}.\n\n"
            "The traveler's interests are: {interests}.\n\n"
            "The itinerary must:\n"
            "1. Start with a **Trip Summary** (destination, dates, total cost, budget status).\n"
            "2. Include a **Cost Breakdown** table.\n"
            "3. Have a section for each day (Day 1, Day 2, etc.) with:\n"
            "   - Morning, Afternoon, and Evening activities.\n"
            "   - Restaurant/food suggestions for each meal.\n"
            "   - Estimated costs for each activity.\n\n"
            "All costs must be shown in {currency} ({currency_symbol}).\n"
            "Format the entire output as clean, well-structured Markdown."
        ),
        expected_output=(
            "A complete, beautifully formatted Markdown travel itinerary with:\n"
            "- Trip Summary header\n"
            "- Cost Breakdown table (in {currency_symbol})\n"
            "- Day-by-day schedule (Day 1 through Day {num_days})\n"
            "- Each day has Morning / Afternoon / Evening sections"
        ),
        agent=compiler,
        context=context_tasks,  # This agent reads the outputs of the previous tasks.
    )
