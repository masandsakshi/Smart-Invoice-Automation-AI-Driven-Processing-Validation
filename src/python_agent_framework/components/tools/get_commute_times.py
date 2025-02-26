# tools/get_commute_times.py

from core.tool import Tool, Parameter
from typing import Dict, Any
import os
from dotenv import load_dotenv
import requests
import time
from datetime import datetime


def convert_to_unix_timestamp(date_str: str) -> int:
    """
    Converts a date-time string to a Unix timestamp assuming local time zone.
    
    Supports multiple formats including:
    - 'YYYY-MM-DD HH:MM:SS'
    - 'YYYY-MM-DDTHH:MM:SS'
    - 'YYYY-MM-DD HH:MM'
    - 'YYYY-MM-DDTHH:MM'

    :param date_str: Date-time string in a supported format
    :return: Unix timestamp as an integer
    """

    possible_formats = [
        "%Y-%m-%d %H:%M:%S",  # Space separator
        "%Y-%m-%dT%H:%M:%S",  # 'T' separator (ISO 8601)
        "%Y-%m-%d %H:%M",     # Space separator, no seconds
        "%Y-%m-%dT%H:%M"      # 'T' separator, no seconds
    ]

    for fmt in possible_formats:
        try:
            dt = datetime.strptime(date_str, fmt)  # Try parsing with each format
            return int(time.mktime(dt.timetuple()))  # Convert to Unix timestamp
        except ValueError:
            continue  # Try the next format if parsing fails

    raise ValueError(f"Unsupported date format: {date_str}")  # Raise error if no formats matched


def get_commute_times(starting_address: str, destination_address: str, departure_time: str) -> Dict[str, Any]:
    """
    Calculates commute times using car, public transit, and biking.

    :param starting_address: Starting address.
    :param destination_address: Destination address.
    :param departure_time: Desired departure time (ISO 8601 format).
    :return: Dictionary containing commute times for different transportation modes.
    """
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    
    try:
        modes = ["driving", "transit", "bicycling"]
        commute_times = {}
        timestamp = convert_to_unix_timestamp(departure_time)
        
        for mode in modes:
            response = requests.get(
                "https://maps.googleapis.com/maps/api/directions/json",
                params={
                    "origin": starting_address,
                    "destination": destination_address,
                    "mode": mode,
                    "departure_time": timestamp,
                    "key": google_api_key
                }
            )
            data = response.json()
            if data["routes"]:
                duration = data["routes"][0]["legs"][0]["duration"]["text"]
                commute_times[mode] = duration
            else:
                commute_times[mode] = "N/A"
        
        return commute_times
    
    except Exception as e:
        return {"error": f"Failed to calculate commute times: {e}"}
    
    
tool = Tool(
    description="Calculate average commute times from a property to a work location using various transportation modes.",
    function=get_commute_times,
    parameters=[
        Parameter(
            name="starting_address",
            type="string",
            description="The starting address.",
            required=True
        ),
        Parameter(
            name="destination_address",
            type="string",
            description="The destination address.",
            required=True
        ),
        Parameter(
            name="departure_time",
            type="string",
            description="The desired departure time for the commute in ISO 8601 format.",
            required=True
        ),
    ],
    metadata={
        "author": "Nathan Angstadt",
        "version": "1.0",
        "category": "Maps",
    }
)