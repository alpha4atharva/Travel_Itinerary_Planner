import os
from crewai.tools import tool
from serpapi import GoogleSearch

@tool("FlightSearchTool")
def search_flights(origin: str, destination: str, date: str) -> str:
    """Useful for finding real-time flight prices and options between two cities. 
    Input should be the origin city, destination city, and the travel date (YYYY-MM-DD)."""
    
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Error: SERPAPI_API_KEY is not set in the environment."

    try:
        # We use standard Google Search to get the flight answer box or organic results
        # since Google Flights engine requires specific IATA codes. 
        # This is a robust way to get flight prices using natural language queries.
        query = f"cheap flights from {origin} to {destination} on {date} one way"
        
        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "gl": "us",
            "hl": "en"
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        output = f"Flight Search Results for {origin} to {destination} on {date}:\n\n"
        
        # Check if Google provided a specific "Flights" widget/answer box
        if "flights" in results:
            flights = results["flights"]
            for f in flights.get("flights", [])[:5]:
                airline = f.get("airline", "Unknown Airline")
                price = f.get("price", "Price unknown")
                duration = f.get("duration", "Duration unknown")
                output += f"- Airline: {airline} | Price: {price} | Duration: {duration}\n"
            return output
            
        # Fallback to organic results snippets
        if "organic_results" in results:
            output += "Organic Results Snippets (Look for prices here):\n"
            for r in results["organic_results"][:5]:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                output += f"- {title}: {snippet}\n"
            return output
            
        return f"No clear flight prices found for {origin} to {destination}."

    except Exception as e:
        return f"Error fetching flights: {str(e)}"

@tool("HotelSearchTool")
def search_hotels(destination: str, check_in_date: str, check_out_date: str) -> str:
    """Useful for finding real-time hotel prices and options in a specific city.
    Input should be the destination city, check-in date (YYYY-MM-DD), and check-out date (YYYY-MM-DD)."""
    
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Error: SERPAPI_API_KEY is not set in the environment."

    try:
        params = {
            "engine": "google_hotels",
            "q": destination,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "api_key": api_key,
            "currency": "USD",
            "gl": "us",
            "hl": "en"
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        output = f"Hotel Search Results for {destination} from {check_in_date} to {check_out_date}:\n\n"
        
        if "properties" in results:
            for h in results["properties"][:10]:
                name = h.get("name", "Unknown Hotel")
                price = h.get("rate_per_night", {}).get("lowest", "Price unknown")
                total = h.get("total_rate", {}).get("lowest", "Total unknown")
                rating = h.get("overall_rating", "No rating")
                class_rating = h.get("hotel_class", "No class rating")
                
                output += f"- Hotel: {name} | Class: {class_rating} | Rating: {rating}/5.0 | Price Per Night: {price} | Total for Stay: {total}\n"
            return output
            
        return f"No clear hotel prices found for {destination}."

    except Exception as e:
        return f"Error fetching hotels: {str(e)}"
