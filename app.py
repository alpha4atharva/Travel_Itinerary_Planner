"""
app.py — Streamlit UI for the Travel Itinerary Planner.

Run with:
    streamlit run app.py
"""

import streamlit as st
import datetime
from dotenv import load_dotenv
load_dotenv()  # Load API keys from .env

from backend.crew import run_crew


# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Travel Itinerary Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Hide sidebar & default Streamlit chrome for a clean look ──────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global Reset ─────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    [data-testid="collapsedControl"] { display: none; }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px;
    }

    /* ── Hero Section ─────────────────────────────────────────── */
    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1rem;
    }

    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }

    .hero p {
        font-size: 1.05rem;
        color: #94a3b8;
        font-weight: 400;
        margin-top: 0;
    }

    /* ── Input Card ───────────────────────────────────────────── */
    .input-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.05), rgba(118,75,162,0.05));
        border: 1px solid rgba(102,126,234,0.15);
        border-radius: 16px;
        padding: 1.5rem 2rem 1rem;
        margin-bottom: 1.5rem;
    }

    /* ── Buttons ──────────────────────────────────────────────── */
    .stButton > button {
        padding: 0.7rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        cursor: pointer;
        transition: all 0.25s ease;
        letter-spacing: 0.3px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35);
    }

    /* ── Download button ─────────────────────────────────────── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.35) !important;
    }

    /* ── Divider ──────────────────────────────────────────────── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102,126,234,0.3), transparent);
        margin: 1.5rem 0;
    }

    /* ── Result Card ─────────────────────────────────────────── */
    .result-header {
        text-align: center;
        padding: 1rem 0;
    }

    .result-header h2 {
        font-size: 1.6rem;
        font-weight: 700;
        color: #334155;
    }

    /* ── Footer ──────────────────────────────────────────────── */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        padding: 2rem 0 1rem;
    }

    .footer a {
        color: #667eea;
        text-decoration: none;
    }

    /* ── Landing Features ────────────────────────────────────── */
    .feature-card {
        background: rgba(102,126,234,0.04);
        border: 1px solid rgba(102,126,234,0.1);
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
        height: 100%;
    }

    .feature-card .icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .feature-card h4 {
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.3rem;
        font-size: 0.95rem;
    }

    .feature-card p {
        font-size: 0.85rem;
        color: #64748b;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)


# ── Currency Config ───────────────────────────────────────────────────────────
CURRENCY_OPTIONS = {
    "INR (₹)": {"code": "INR", "symbol": "₹"},
    "USD ($)": {"code": "USD", "symbol": "$"},
    "EUR (€)": {"code": "EUR", "symbol": "€"},
    "GBP (£)": {"code": "GBP", "symbol": "£"},
}


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🌍 AI Travel Itinerary Planner</h1>
    <p>Enter your trip details below and get a personalized, budget-aware itinerary in minutes.</p>
</div>
""", unsafe_allow_html=True)


# ── Input Form (Top Bar Style) ───────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)

# Row 1: Origin, Destination, Currency
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.markdown("**🏠 Origin City**")
    origin = st.text_input("Origin", placeholder="e.g., Mumbai, India", label_visibility="collapsed",
                           help="Where are you traveling from?", key="origin_input")
with col2:
    st.markdown("**🎯 Destination**")
    destination = st.text_input("Destination", placeholder="e.g., Paris, France", label_visibility="collapsed",
                                help="Where do you want to go?", key="dest_input")
with col3:
    st.markdown("**💱 Currency**")
    currency_label = st.selectbox("Currency", options=list(CURRENCY_OPTIONS.keys()), index=0,
                                  label_visibility="collapsed", key="currency_select")
    currency = CURRENCY_OPTIONS[currency_label]

# Row 2: Budget, Travelers, Start Date, Days
col4, col5, col6, col7 = st.columns(4)
with col4:
    st.markdown(f"**💰 Budget / Person ({currency['symbol']})**")
    budget = st.number_input(
        f"Budget per Person ({currency['code']})",
        min_value=100, max_value=10000000,
        value=50000 if currency["code"] == "INR" else 2500,
        step=500 if currency["code"] == "INR" else 100,
        label_visibility="collapsed",
        help=f"Your trip budget PER PERSON in {currency['code']}.",
    )
with col5:
    st.markdown("**👥 Travelers**")
    num_persons = st.number_input("Travelers", min_value=1, max_value=20, value=1, step=1,
                                  label_visibility="collapsed", help="How many people are traveling?")
with col6:
    st.markdown("**🛫 Start Date**")
    start_date = st.date_input("Start Date", min_value=datetime.date.today(),
                               label_visibility="collapsed", help="When does your trip start?")
with col7:
    st.markdown("**📅 Days**")
    num_days = st.number_input("Days", min_value=1, max_value=30, value=5, step=1,
                               label_visibility="collapsed", help="How many days is your trip?")

# Row 3: Interests
st.markdown("**🎯 Travel Interests**")
interests = st.multiselect(
    "Travel Interests",
    options=[
        "History & Culture", "Food & Drink", "Adventure & Outdoors",
        "Nightlife & Entertainment", "Nature & Wildlife", "Shopping",
        "Art & Museums", "Relaxation & Wellness",
    ],
    default=["History & Culture", "Food & Drink"],
    label_visibility="collapsed",
    help="Select your interests to personalize the itinerary.",
)

# Row 4: Generate Button (centered)
bcol1, bcol2, bcol3 = st.columns([1, 1, 1])
with bcol2:
    generate_btn = st.button("🚀  Generate My Itinerary", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ── Generation Logic ─────────────────────────────────────────────────────────
if generate_btn:
    if not origin or not origin.strip():
        st.error("⚠️ Please enter your origin city.")
    elif not destination or not destination.strip():
        st.error("⚠️ Please enter your destination.")
    else:
        total_budget = int(budget) * int(num_persons)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        status_text = (
            f"Planning a **{num_days}-day** trip from **{origin}** → **{destination}** "
            f"for **{num_persons}** traveler{'s' if num_persons > 1 else ''} · "
            f"Budget: **{currency['symbol']}{budget:,}**/person · "
            f"Total: **{currency['symbol']}{total_budget:,}**"
        )
        st.info(f"✈️ {status_text}")

        with st.spinner("⏳ Generating your personalized itinerary... This may take 1–2 minutes."):
            try:
                result = run_crew(
                    origin=origin.strip(),
                    destination=destination.strip(),
                    budget=int(budget),
                    num_persons=int(num_persons),
                    currency=currency["code"],
                    currency_symbol=currency["symbol"],
                    start_date=start_date.strftime("%Y-%m-%d"),
                    num_days=int(num_days),
                    interests=", ".join(interests) if interests else "General sightseeing",
                )
                st.session_state["itinerary"] = result
                st.session_state["destination"] = destination.strip()

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
                st.info(
                    "💡 **Troubleshooting tips:**\n"
                    "- Make sure your `GEMINI_API_KEY` and `SERPER_API_KEY` are set in the `.env` file.\n"
                    "- Check that you have an active internet connection.\n"
                    "- Try reducing the number of days if the request is too complex."
                )


# ── Display Saved Itinerary ──────────────────────────────────────────────────
if "itinerary" in st.session_state:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.success("✅ Your itinerary is ready!")

    st.markdown(st.session_state["itinerary"])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Action buttons
    dcol1, dcol2, dcol3 = st.columns([1, 1, 1])
    with dcol1:
        st.download_button(
            label="📥  Download as Markdown",
            data=st.session_state["itinerary"],
            file_name=f"itinerary_{st.session_state['destination'].replace(' ', '_').lower()}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with dcol3:
        if st.button("🗑️  Clear & Start Over", use_container_width=True):
            del st.session_state["itinerary"]
            del st.session_state["destination"]
            st.rerun()

elif not generate_btn:
    # ── Landing — Feature Cards ──────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🔍</div>
            <h4>Smart Research</h4>
            <p>AI searches the web for attractions, restaurants, and local tips tailored to your interests.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">💰</div>
            <h4>Budget Aware</h4>
            <p>Compares multiple flight, hotel, and package options across budget tiers.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">📋</div>
            <h4>Day-by-Day Plan</h4>
            <p>Get a detailed itinerary with morning, afternoon, and evening activities.</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">💱</div>
            <h4>Dual Currency</h4>
            <p>All prices shown in your currency and the destination's local currency.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Fill in your trip details above and click <b>Generate My Itinerary</b> to get started.
    </div>
    """, unsafe_allow_html=True)
