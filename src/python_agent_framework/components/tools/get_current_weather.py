# tools/get_current_weather.py

from core.tool import Tool, Parameter
from typing import Dict, Any
import os
from dotenv import load_dotenv
import requests


def get_current_weather(location: str, unit: str) -> str:
    """
    Fetches the current weather for the specified location.

    :param location: The location for which to get the weather.
    :param unit: Temperature unit ('celsius' or 'fahrenheit').
    :return: A string describing the current weather.
    """
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    units = "metric" if unit == "celsius" else "imperial"
    try:
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params={
                "q": location,
                "appid": api_key,
                "units": units
            }
        )
        
        if response.status_code != 404:
            data = response.json()
            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            return f"The current weather in {location} is {weather} with a temperature of {temp}°{'C' if units == 'metric' else 'F'}."
        else:
            return f"Failed to get the current weather in {location}. {response.reason}"
    except Exception as e:
        return f"Failed to retrieve weather data: {e}"


tool = Tool(
    description="Retrieves weather data for a given location.",
    function=get_current_weather,
    parameters=[
        Parameter(
            name="location",
            type="string",
            description="The city and state with no abbreviations, e.g., San Francisco, California.",
            required=True
        ),
        Parameter(
            name="unit",
            type="string",
            description="The temperature unit to use.",
            enum=["celsius", "fahrenheit"],
            required=True
        ),
    ],
    metadata={
        "author": "Nathan Angstadt",
        "version": "1.0",
        "category": "Weather",
    }
)