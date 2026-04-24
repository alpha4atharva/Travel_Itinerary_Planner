"""
crew.py — Assembles the CrewAI agents and tasks into a working Crew.

This is the main entry point for the backend logic. Call `run_crew()`
with the user's inputs to kick off the multi-agent planning pipeline.
"""

from crewai import Crew, Process
from backend.agents import (
    create_travel_researcher,
    create_logistics_manager,
    create_itinerary_compiler,
)
from backend.tasks import (
    create_research_task,
    create_logistics_task,
    create_compilation_task,
)


def run_crew(
    origin: str,
    destination: str,
    budget: int,
    currency: str,
    currency_symbol: str,
    start_date: str,
    num_days: int,
    interests: str = "General sightseeing",
) -> str:
    """Assembles and kicks off the Travel Planner crew.

    Args:
        origin:          The city/airport the user is traveling from.
        destination:     The travel destination.
        budget:          Total trip budget in the chosen currency.
        currency:        Currency code (e.g., INR, USD, EUR, GBP).
        currency_symbol: Currency symbol (e.g., ₹, $, €, £).
        start_date:      Trip start date in YYYY-MM-DD format.
        num_days:        Number of days for the trip.
        interests:       Comma-separated travel interests.

    Returns:
        The final itinerary as a Markdown-formatted string.
    """
    # ── Step 1: Create Agents ─────────────────────────────────────────────
    researcher = create_travel_researcher()
    logistics_manager = create_logistics_manager()
    compiler = create_itinerary_compiler()

    # ── Step 2: Create Tasks ──────────────────────────────────────────────
    # Research and Logistics tasks run in parallel (async_execution=True)
    # to cut total wait time nearly in half.
    research_task = create_research_task(researcher)
    logistics_task = create_logistics_task(logistics_manager)
    compilation_task = create_compilation_task(
        compiler,
        context_tasks=[research_task, logistics_task],
    )

    # ── Step 3: Assemble the Crew ─────────────────────────────────────────
    crew = Crew(
        agents=[researcher, logistics_manager, compiler],
        tasks=[research_task, logistics_task, compilation_task],
        process=Process.sequential,  # Agents work one after another.
        verbose=True,
    )

    # ── Step 4: Kick Off ──────────────────────────────────────────────────
    # The input dict values replace {origin}, {destination}, etc. in the
    # agent goals and task descriptions.
    result = crew.kickoff(
        inputs={
            "origin": origin,
            "destination": destination,
            "budget": budget,
            "currency": currency,
            "currency_symbol": currency_symbol,
            "start_date": start_date,
            "num_days": num_days,
            "interests": interests,
        }
    )

    return str(result)
