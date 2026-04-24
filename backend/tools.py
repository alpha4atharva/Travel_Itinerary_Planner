import os
from crewai.tools import tool
from serpapi import GoogleSearch

@tool("FlightSearchTool")
def search_flights(origin: str, destination: str, date: str) -> str:
    """Useful for finding real-time flight prices and options between two cities.
    Input should be the origin IATA airport code (e.g. 'DEL' for Delhi, 'JFK' for New York), 
    destination IATA airport code (e.g. 'NRT' for Tokyo, 'CDG' for Paris), 
    and the travel date in YYYY-MM-DD format.
    If you don't know the IATA code, use the main airport code for that city."""
    
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Error: SERPAPI_API_KEY is not set in the environment."

    try:
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": date,
            "type": "2",            # 2 = one-way
            "currency": "USD",
            "hl": "en",
            "api_key": api_key,
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        output = f"Flight Search Results for {origin} → {destination} on {date}:\n\n"
        
        # Collect flights from both best_flights and other_flights
        all_flights = []
        for flight_group in results.get("best_flights", []):
            all_flights.append(flight_group)
        for flight_group in results.get("other_flights", []):
            all_flights.append(flight_group)
        
        if not all_flights:
            return f"No flights found for {origin} to {destination} on {date}. Please verify the IATA airport codes are correct."
        
        for i, flight_group in enumerate(all_flights[:10], 1):
            price = flight_group.get("price", "N/A")
            total_duration = flight_group.get("total_duration", "N/A")
            segments = flight_group.get("flights", [])
            stops = len(segments) - 1
            stop_label = "Non-stop" if stops == 0 else f"{stops} stop(s)"
            
            # Get airline name(s) from segments
            airlines = []
            for seg in segments:
                airline = seg.get("airline", "Unknown")
                if airline not in airlines:
                    airlines.append(airline)
            airline_str = ", ".join(airlines)
            
            output += f"Option {i}: {airline_str} | ${price} USD | {total_duration} min | {stop_label}\n"
        
        return output

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
