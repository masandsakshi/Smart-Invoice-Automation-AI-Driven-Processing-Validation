# tools/get_n_daya_weather_forecast.py

from core.tool import Tool, Parameter
from typing import Dict, Any
import os
from dotenv import load_dotenv
import requests


def get_n_day_weather_forecast(location: str, unit: str, num_days: int) -> str:
    """
    Fetches the N-day weather forecast for the specified location.

    :param location: The location for which to get the forecast.
    :param unit: Temperature unit ('celsius' or 'fahrenheit').
    :param num_days: Number of days for the forecast.
    :return: A string describing the weather forecast.
    """
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    # Input validation
    if num_days < 1 or num_days > 7:
        return "Please specify a number of days between 1 and 7."
    
    units = "metric" if unit == "celsius" else "imperial"
    try:
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/forecast",
            params={
                "q": location,
                "appid": api_key,
                "units": units,
                "cnt": num_days * 8  # OpenWeatherMap provides data in 3-hour intervals
            }
        )
        data = response.json()
        forecast_list = data.get("list", [])
        if not forecast_list:
            return "No forecast data available."
        
        forecast = f"Weather forecast for {location} over the next {num_days} day(s):\n"
        for entry in forecast_list:
            dt_txt = entry["dt_txt"]
            weather = entry["weather"][0]["description"].capitalize()
            temp = entry["main"]["temp"]
            forecast += f"{dt_txt}: {weather}, {temp}°{'C' if units == 'metric' else 'F'}\n"
        return forecast
    except Exception as e:
        return f"Failed to retrieve weather forecast data: {e}"


tool = Tool(
    description="Get an N-day weather forecast for a specified location.",
    function=get_n_day_weather_forecast,
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
        Parameter(
            name="num_days",
            type="integer",
            description="The number of days to forecast (1-7).",
            required=True
        )
    ],
    metadata={
        "author": "Nathan Angstadt",
        "version": "1.0",
        "category": "Weather",
    }
)