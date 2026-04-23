# 🌍 AI Travel Itinerary Planner

A multi-agent AI system that generates detailed, budget-aware, day-by-day travel itineraries using **CrewAI**, **Google Gemini**, and **Serper** web search.

## Architecture

This project uses a **3-agent pipeline** powered by CrewAI:

| Agent | Role | What It Does |
|-------|------|-------------|
| 🔍 **Travel Researcher** | Destination Expert | Searches the web for top attractions, restaurants, local tips, and hidden gems. |
| 💼 **Logistics Manager** | Budget Coordinator | Finds flight & hotel prices, calculates total costs, and verifies the budget. |
| 📋 **Itinerary Compiler** | Master Planner | Combines all research into a polished, day-by-day Markdown itinerary. |

The agents work **sequentially** — the Researcher and Logistics Manager do their work first, then the Compiler reads their outputs and creates the final plan.

## Tech Stack

- **Python** — Core language
- **CrewAI** — Multi-agent orchestration framework
- **Google Gemini** — LLM (gemini-2.0-flash)
- **Serper API** — Google search for real-time web data
- **Streamlit** — Web UI

## Setup

### 1. Create & activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API keys
Edit the `.env` file and paste your keys:
```env
GEMINI_API_KEY=your_gemini_key_here
SERPER_API_KEY=your_serper_key_here
```

- **Gemini API Key:** Get it free from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Serper API Key:** Get 2,500 free searches from [serper.dev](https://serper.dev)

## Usage

### Run with Streamlit UI
```bash
streamlit run app.py
```

### Run in terminal (for testing)
```bash
python main.py
```

## Project Structure

```
Travel_Itinerary_Planner/
├── .env                  # API Keys (not committed to git)
├── .gitignore
├── requirements.txt
├── README.md
├── app.py                # Streamlit web interface
├── main.py               # Terminal test script
└── backend/
    ├── __init__.py
    ├── agents.py         # 3 CrewAI agent definitions
    ├── tasks.py          # Task definitions for each agent
    └── crew.py           # Assembles agents + tasks into a Crew
```
