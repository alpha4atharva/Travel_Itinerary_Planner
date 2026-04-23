"""
app.py — Streamlit UI for the Travel Itinerary Planner.

Run with:
    streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv
load_dotenv()  # Load API keys from .env

from backend.crew import run_crew


# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Travel Itinerary Planner",
    page_icon="🌍",
    layout="wide",
)

# ── Custom Styling ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }

    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }

    .main-header p {
        font-size: 1.1rem;
        color: #888;
    }

    .stButton > button {
        width: 100%;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .sidebar .stNumberInput, .sidebar .stTextInput {
        margin-bottom: 0.5rem;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🌍 AI Travel Itinerary Planner</h1>
    <p>Powered by CrewAI Multi-Agent System & Google Gemini</p>
</div>
""", unsafe_allow_html=True)


# ── Sidebar — User Inputs ────────────────────────────────────────────────────
with st.sidebar:
    st.header("✈️ Plan Your Trip")
    st.markdown("---")

    origin = st.text_input(
        "🏠 Origin City / Airport",
        placeholder="e.g., Mumbai, India",
        help="Where are you traveling from?",
    )

    destination = st.text_input(
        "🎯 Destination",
        placeholder="e.g., Tokyo, Japan",
        help="Where do you want to go?",
    )

    budget = st.number_input(
        "💰 Total Budget (INR)",
        min_value=5000,
        max_value=1000000,
        value=50000,
        step=5000,
        help="Your total trip budget in Rupees including flights, hotels, food, and activities.",
    )

    num_days = st.number_input(
        "📅 Number of Days",
        min_value=1,
        max_value=30,
        value=5,
        step=1,
        help="How many days is your trip?",
    )

    st.markdown("---")
    generate_btn = st.button("🚀 Generate Itinerary", type="primary")


# ── Main Area — Results ──────────────────────────────────────────────────────
if generate_btn:
    # Validate inputs
    if not origin.strip():
        st.error("⚠️ Please enter your origin city.")
    elif not destination.strip():
        st.error("⚠️ Please enter your destination.")
    else:
        # Show agent status
        st.info(
            f"🤖 **Crew assembled!** Three AI agents are now planning your "
            f"{num_days}-day trip from **{origin}** to **{destination}** "
            f"with a budget of **₹{budget:,}**."
        )

        with st.spinner("⏳ Agents are researching, calculating, and compiling your itinerary... This may take 1-2 minutes."):
            try:
                result = run_crew(
                    origin=origin.strip(),
                    destination=destination.strip(),
                    budget=int(budget),
                    num_days=int(num_days),
                )

                st.success("✅ Your itinerary is ready!")
                st.markdown("---")
                st.markdown(result)

                # Download button
                st.download_button(
                    label="📥 Download Itinerary as Markdown",
                    data=result,
                    file_name=f"itinerary_{destination.replace(' ', '_').lower()}.md",
                    mime="text/markdown",
                )

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
                st.info(
                    "💡 **Troubleshooting tips:**\n"
                    "- Make sure your `GROQ_API_KEY` and `SERPER_API_KEY` are set in the `.env` file.\n"
                    "- Check that you have an active internet connection.\n"
                    "- Try reducing the number of days if the request is too complex."
                )

else:
    # Landing state — show instructions
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔍 Agent 1: Researcher")
        st.markdown(
            "Searches the web for top attractions, restaurants, "
            "local customs, and hidden gems at your destination."
        )

    with col2:
        st.markdown("### 💼 Agent 2: Budget Manager")
        st.markdown(
            "Finds real flight and hotel prices, calculates total costs, "
            "and ensures everything fits within your budget."
        )

    with col3:
        st.markdown("### 📋 Agent 3: Planner")
        st.markdown(
            "Combines all the research into a polished, day-by-day "
            "itinerary with meals, activities, and cost breakdown."
        )

    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #888;'>"
        "👈 Fill in your trip details in the sidebar and click <b>Generate Itinerary</b> to start!"
        "</p>",
        unsafe_allow_html=True,
    )
