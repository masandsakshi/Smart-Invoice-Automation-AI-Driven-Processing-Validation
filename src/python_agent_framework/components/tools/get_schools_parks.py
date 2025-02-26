# tools/get_schools_parks.py

from core.tool import Tool, Parameter
from typing import Dict, Any
import json
import os
from dotenv import load_dotenv
import requests


def get_schools_parks(address: str, radius: float) -> Dict[str, Any]:
    """
    Fetches schools and parks within a specified radius of the given address.

    :param address: The address to search around.
    :param radius: Radius in meters.
    :return: Dictionary containing lists of nearby schools and parks.
    """
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    
    try:
        # Geocode the address to get latitude and longitude
        geocode_response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={
                "address": address,
                "key": google_api_key
            }
        )
        geocode_data = geocode_response.json()
        location = geocode_data["results"][0]["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]
        
        # Search for schools
        schools_response = requests.get(
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params={
                "location": f"{lat},{lng}",
                "radius": radius,
                "type": "school",
                "key": google_api_key
            }
        )
        schools_data = schools_response.json()
        schools = [place["name"] for place in schools_data.get("results", [])]
        
        # Search for parks
        parks_response = requests.get(
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params={
                "location": f"{lat},{lng}",
                "radius": radius,
                "type": "park",
                "key": google_api_key
            }
        )
        parks_data = parks_response.json()
        parks = [place["name"] for place in parks_data.get("results", [])]
        
    
        # response_data = {
        #     'schools': schools,
        #     'parks': parks
        # }
        # json_content = json.dumps(response_data, indent=None)  # Convert dict to JSON string
        # return json_content
        return {"schools": schools, "parks": parks}
    
    except Exception as e:
        return {"error": f"Failed to retrieve schools and parks data: {e}"}


tool = Tool(
    description="Retrieve schools and parks within walking distance of a given location.",
    function=get_schools_parks,
    parameters=[
        Parameter(
            name="address",
            type="string",
            description="The address around which to search for schools and parks.",
            required=True
        ),
        Parameter(
            name="radius",
            type="number",
            description="The radius in meters to search for schools and parks.",
            required=True
        ),
    ],
    metadata={
        "author": "Nathan Angstadt",
        "version": "1.0",
        "category": "Maps",
    }
)
