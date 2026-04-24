"""
agents.py — Defines the 3 CrewAI Agents for the Travel Itinerary Planner.

Agents:
    1. Travel Researcher      — Finds attractions, restaurants, and local tips.
    2. Logistics Manager       — Finds flights, hotels, and manages budget.
    3. Itinerary Compiler      — Combines everything into a day-by-day plan.
"""

import os
from crewai import Agent, LLM
from crewai_tools import SerperDevTool
from crewai.tools import tool

# ── Tool Setup ───────────────────────────────────────────────────────────────
# SerperDevTool allows agents to perform Google searches.
# Requires SERPER_API_KEY to be set in the environment / .env file.
search_tool = SerperDevTool()

@tool("CalculatorTool")
def calculate(expression: str) -> str:
    """Useful for performing mathematical calculations. Use this for adding up flights, hotels, and daily expenses. Input should be a mathematical expression like '2000 + 1500 * 3'."""
    try:
        # Safe eval using limited locals/globals to prevent arbitrary code execution
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error calculating: {e}"

# ── LLM Setup ────────────────────────────────────────────────────────────────
# Using Gemini 2.5 Flash
# Requires GEMINI_API_KEY to be set in the environment / .env file.
gemini_llm = LLM(
    model="gemini/gemini-3.1-flash-lite-preview",
    temperature=0.7,
)


# ── Agent Definitions ────────────────────────────────────────────────────────

def create_travel_researcher() -> Agent:
    """Creates the Travel Researcher agent.

    This agent specializes in exploring destinations — finding the best
    attractions, local cuisine, cultural tips, and hidden gems.
    """
    return Agent(
        role="Destination Expert",
        goal=(
            "Research and discover the top attractions, must-try restaurants, "
            "local customs, weather conditions, and hidden gems in {destination}. "
            "Provide practical tips that a real traveler would find invaluable."
        ),
        backstory=(
            "You are a seasoned travel blogger with over 15 years of experience "
            "exploring destinations around the world. You have a knack for finding "
            "hidden gems that most tourists miss, and you always provide practical, "
            "honest recommendations. You know how to balance popular landmarks with "
            "off-the-beaten-path experiences."
        ),
        tools=[search_tool],
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False,
        max_rpm=3,
    )


def create_logistics_manager() -> Agent:
    """Creates the Logistics & Budget Manager agent.

    This agent handles the financial side — finding flight costs, hotel
    prices, and ensuring everything fits within the user's budget.
    """
    return Agent(
        role="Travel Logistics Coordinator",
        goal=(
            "Find specific travel options (flights, trains, or buses) from {origin} to {destination} for the travel date {start_date}. "
            "Find 2-3 specific hotels in {destination} for {num_days} days. "
            "You MUST provide the actual names of the airlines/trains and hotels. Do not use generic averages. "
            "Calculate the total estimated cost for travel and accommodation using the CalculatorTool, and "
            "verify that it stays within the total budget of ₹{budget}. "
            "If the budget is tight, suggest cheaper alternatives."
        ),
        backstory=(
            "You are a meticulous financial planner and travel deal expert. "
            "You have spent years helping travelers get the best bang for their buck. "
            "You excel at finding budget-friendly flights, comparing hotel prices, "
            "and creating realistic cost breakdowns. You never let a trip go over budget."
        ),
        tools=[search_tool, calculate],
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False,
        max_rpm=3,
    )


def create_itinerary_compiler() -> Agent:
    """Creates the Itinerary Compiler agent.

    This agent takes the research and logistics data from the other two
    agents and compiles a beautifully formatted, day-by-day itinerary.
    """
    return Agent(
        role="Master Travel Planner",
        goal=(
            "Compile all the research about {destination} and the logistics/budget "
            "information into a cohesive, detailed, day-by-day travel itinerary "
            "for {num_days} days. The itinerary must include a clear cost breakdown "
            "and stay within the budget of ₹{budget}."
        ),
        backstory=(
            "You are an expert travel agent renowned for creating beautiful, "
            "easy-to-read, and perfectly scheduled travel plans. You know how to "
            "balance sightseeing, relaxation, and dining into a realistic daily "
            "schedule. Your itineraries are so well-organized that travelers never "
            "feel rushed or lost."
        ),
        tools=[calculate],  # Give compiler access to calculator just in case
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False,
        max_rpm=3,
    )
