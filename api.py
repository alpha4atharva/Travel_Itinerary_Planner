import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the existing crew logic
from backend.crew import run_crew

app = FastAPI(title="Travel Itinerary API")

# Define the request model
class TripRequest(BaseModel):
    origin: str
    destination: str
    budget: int
    num_persons: int
    currency: str
    currency_symbol: str
    start_date: str
    num_days: int
    interests: str

# Serve the static files directory
# We ensure the static directory exists so FastAPI doesn't crash on startup
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    """Serves the main HTML file on the root route."""
    return FileResponse("static/index.html")

@app.post("/api/generate")
async def generate_itinerary(request: TripRequest):
    """
    Endpoint to trigger the CrewAI agents and return the markdown itinerary.
    """
    try:
        # We run this synchronously since crew.kickoff is synchronous
        result = run_crew(
            origin=request.origin,
            destination=request.destination,
            budget=request.budget,
            num_persons=request.num_persons,
            currency=request.currency,
            currency_symbol=request.currency_symbol,
            start_date=request.start_date,
            num_days=request.num_days,
            interests=request.interests,
        )
        return {"itinerary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # This allows you to run `python api.py` to start the server
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
