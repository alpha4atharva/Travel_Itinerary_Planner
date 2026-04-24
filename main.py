"""
main.py — Quick terminal test for the Travel Planner crew.

Run this to test the backend without the Streamlit UI:
    python main.py
"""

import sys
import io

# Fix UnicodeEncodeError on Windows terminals (cp1252 can't handle emoji)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from dotenv import load_dotenv
load_dotenv()  # Load API keys from .env

from backend.crew import run_crew


if __name__ == "__main__":
    print("=" * 60)
    print("  🌍 Travel Itinerary Planner — Terminal Test")
    print("=" * 60)

    # ── Sample Inputs (change these to test) ──────────────────────────────
    origin = "Mumbai, India"
    destination = "Tokyo, Japan"
    budget = 2500
    start_date = "2026-05-10"
    num_days = 5

    print(f"\n📍 Origin:      {origin}")
    print(f"🎯 Destination: {destination}")
    print(f"💰 Budget:      ${budget}")
    print(f"📅 Duration:    {num_days} days")
    print("\n⏳ Agents are working... This may take 1-2 minutes.\n")

    result = run_crew(
        origin=origin,
        destination=destination,
        budget=budget,
        start_date=start_date,
        num_days=num_days,
    )

    print("\n" + "=" * 60)
    print("  ✅ FINAL ITINERARY")
    print("=" * 60)
    print(result)
