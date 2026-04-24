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
            "Find realistic and SPECIFIC cost estimates for a ROUND-TRIP from {origin} to {destination} "
            "starting on {start_date} for {num_days} days for {num_persons} person(s).\n\n"
            "Budget: {currency_symbol}{budget_per_person} per person × {num_persons} person(s) = "
            "{currency_symbol}{total_budget} total.\n\n"
            "IMPORTANT CURRENCY RULE: Show ALL prices in BOTH:\n"
            "  - The user's currency: {currency} ({currency_symbol})\n"
            "  - The destination country's local currency\n"
            "If they are the same currency, show only one.\n"
            "Use approximate current exchange rates.\n\n"
            "You must research and provide MULTIPLE OPTIONS for each category:\n\n"
            "1. **Travel (Flights/Trains/Buses) — ONE-WAY:** You MUST use the `FlightSearchTool` to fetch real flight options and prices from {origin} to {destination} for {start_date}.\n"
            "   *Note: If flights are not applicable (e.g., short distances), use your general Search tool to find estimated Train/Bus prices and explicitly label them as '(Estimated)'*\n"
            "   For EACH option, provide:\n"
            "   - **Route:** {origin} → {destination} — Airline/Train name, class, and price PER PERSON.\n"
            "   Include a mix of budget and premium options.\n\n"
            "2. **Accommodation:** You MUST use the `HotelSearchTool` to fetch real hotel prices in {destination}. "
            "For each hotel provide: Hotel name, star rating, location/area, nightly rate PER ROOM, "
            "and total cost for {num_days} nights. "
            "Include Budget, Mid-Range, and Premium options.\n\n"
            "3. **Daily Expenses:** Estimated daily food and local transport costs PER PERSON. "
            "Provide a breakdown: breakfast, lunch, dinner, and local transport.\n\n"
            "4. **Total Cost Estimates:** Provide 3 different trip packages for ALL {num_persons} person(s):\n"
            "   - 💰 **Budget Package:** Cheapest ONE-WAY flight × {num_persons} + budget hotel + daily expenses × {num_persons} = TOTAL\n"
            "   - ⭐ **Mid-Range Package:** Mid-price ONE-WAY flight × {num_persons} + mid-range hotel + daily expenses × {num_persons} = TOTAL\n"
            "   - 👑 **Premium Package:** Best ONE-WAY flight × {num_persons} + premium hotel + daily expenses × {num_persons} = TOTAL\n\n"
            "5. **Budget Check:** Compare each package total against the total budget of {currency_symbol}{total_budget}.\n"
            "   - Clearly mark which packages are within budget and which are over."
        ),
        expected_output=(
            "A detailed cost comparison in markdown format with:\n\n"
            "**✈️ One-Way Flight / Train Options (comparison table — price per person):**\n"
            "| Option | Route | Airline/Train | Class | Price ({currency_symbol}) | Local Currency |\n"
            "| 1 | {origin} → {destination} | [Name] | Economy | {currency_symbol}XXX | local XXX |\n"
            "| 2 | ... | ... | ... | ... | ... |\n"
            "| 3 | ... | ... | ... | ... | ... |\n\n"
            "**🏨 Hotel Options (comparison table — per room per night):**\n"
            "| Option | Hotel Name | Rating | Nightly Rate ({currency_symbol}) | Local Currency | Total ({num_days} nights) |\n"
            "| Budget | [Name] | ⭐⭐ | {currency_symbol}XXX | local XXX | {currency_symbol}XXX |\n"
            "| Mid-Range | [Name] | ⭐⭐⭐ | {currency_symbol}XXX | local XXX | {currency_symbol}XXX |\n"
            "| Premium | [Name] | ⭐⭐⭐⭐ | {currency_symbol}XXX | local XXX | {currency_symbol}XXX |\n\n"
            "**🍽️ Daily Expenses Breakdown (per person per day):**\n"
            "- Breakfast / Lunch / Dinner / Transport\n\n"
            "**📊 Package Comparison (total for {num_persons} person(s), including one-way flights):**\n"
            "| Package | One-way Flights | Hotel | Daily Exp. | TOTAL | Budget Status |\n"
            "| 💰 Budget | ... | ... | ... | {currency_symbol}XXX | ✅/⚠️ |\n"
            "| ⭐ Mid-Range | ... | ... | ... | {currency_symbol}XXX | ✅/⚠️ |\n"
            "| 👑 Premium | ... | ... | ... | {currency_symbol}XXX | ✅/⚠️ |\n"
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
            "{num_days} days in {destination}, starting on {start_date}, "
            "for {num_persons} person(s).\n\n"
            "The traveler's interests are: {interests}.\n"
            "Budget: {currency_symbol}{budget_per_person} per person "
            "(Total: {currency_symbol}{total_budget}).\n\n"
            "IMPORTANT CURRENCY RULE: Show ALL prices in BOTH:\n"
            "  - The user's currency: {currency} ({currency_symbol})\n"
            "  - The destination country's local currency\n"
            "If they are the same currency, show only one.\n\n"
            "The itinerary must:\n"
            "1. Start with a **Trip Summary** (destination, dates, num travelers, budget per person, total budget).\n"
            "2. Include the **Flight/Train Options** comparison table from the logistics report — "
            "keep ALL options, do NOT collapse them into one. Show dual currencies.\n"
            "3. Include the **Hotel Options** comparison table — keep ALL options with names, ratings, and prices in dual currencies.\n"
            "4. Include the **Package Comparison** table (Budget / Mid-Range / Premium) with totals for all {num_persons} travelers.\n"
            "5. Include a **Daily Expenses Breakdown** (breakfast, lunch, dinner, transport) per person in dual currencies.\n"
            "6. Have a section for each day (Day 1, Day 2, etc.) with:\n"
            "   - Morning, Afternoon, and Evening activities.\n"
            "   - Restaurant/food suggestions for each meal.\n"
            "   - Estimated costs for each activity in dual currencies.\n\n"
            "IMPORTANT: Do NOT reduce the cost breakdown to a single option. "
            "The traveler wants to see ALL options to compare and choose.\n"
            "Format the entire output as clean, well-structured Markdown."
        ),
        expected_output=(
            "A complete, beautifully formatted Markdown travel itinerary with:\n"
            "- Trip Summary header (including {num_persons} travelers and budget)\n"
            "- Flight/Train Options comparison table (5-10 options, dual currency)\n"
            "- Hotel Options comparison table (5-10 options with names and prices, dual currency)\n"
            "- Package Comparison table (Budget / Mid-Range / Premium totals for all travelers)\n"
            "- Daily Expenses Breakdown (per person, dual currency)\n"
            "- Day-by-day schedule (Day 1 through Day {num_days})\n"
            "- Each day has Morning / Afternoon / Evening sections with costs in dual currencies"
        ),
        agent=compiler,
        context=context_tasks,  # This agent reads the outputs of the previous tasks.
    )
