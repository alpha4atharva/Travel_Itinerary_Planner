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

# ── Tool Setup ───────────────────────────────────────────────────────────────
# SerperDevTool allows agents to perform Google searches.
# Requires SERPER_API_KEY to be set in the environment / .env file.
search_tool = SerperDevTool()

# ── LLM Setup ────────────────────────────────────────────────────────────────
# Using Groq's Llama 3.3 70B model (fast and free tier available).
# Requires GROQ_API_KEY to be set in the environment / .env file.
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
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
        llm=groq_llm,
        verbose=True,
        allow_delegation=False,
    )


def create_logistics_manager() -> Agent:
    """Creates the Logistics & Budget Manager agent.

    This agent handles the financial side — finding flight costs, hotel
    prices, and ensuring everything fits within the user's budget.
    """
    return Agent(
        role="Travel Logistics Coordinator",
        goal=(
            "Find estimated round-trip flight costs from {origin} to {destination}, "
            "and average nightly hotel prices in {destination} for {num_days} days. "
            "Calculate the total estimated cost for travel and accommodation, and "
            "verify that it stays within the total budget of ${budget}. "
            "If the budget is tight, suggest cheaper alternatives."
        ),
        backstory=(
            "You are a meticulous financial planner and travel deal expert. "
            "You have spent years helping travelers get the best bang for their buck. "
            "You excel at finding budget-friendly flights, comparing hotel prices, "
            "and creating realistic cost breakdowns. You never let a trip go over budget."
        ),
        tools=[search_tool],
        llm=groq_llm,
        verbose=True,
        allow_delegation=False,
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
            "and stay within the budget of ${budget}."
        ),
        backstory=(
            "You are an expert travel agent renowned for creating beautiful, "
            "easy-to-read, and perfectly scheduled travel plans. You know how to "
            "balance sightseeing, relaxation, and dining into a realistic daily "
            "schedule. Your itineraries are so well-organized that travelers never "
            "feel rushed or lost."
        ),
        tools=[],  # No tools needed — works from the other agents' outputs.
        llm=groq_llm,
        verbose=True,
        allow_delegation=False,
    )
