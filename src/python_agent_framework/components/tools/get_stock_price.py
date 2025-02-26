# tools/get_stock_price.py

from core.tool import Tool, Parameter
from typing import Dict, Any
import os
from dotenv import load_dotenv
import requests


def get_stock_price(ticker: str, currency: str) -> str:
    """
    Fetches the current stock price for the specified ticker symbol.

    :param ticker: Stock ticker symbol.
    :param format: Currency format ('usd' or 'eur').
    :return: A string describing the current stock price.
    """
    load_dotenv()
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    currency = "USD" if format == "usd" else "EUR"
    try:
        response = requests.get(
            "https://www.alphavantage.co/query",
            params={
                "function": "GLOBAL_QUOTE",
                "symbol": ticker,
                "apikey": api_key
            }
        )
        data = response.json()
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            price = data["Global Quote"]["05. price"]
            return f"The current stock price for {ticker.upper()} is {price} {currency}."
        else:
            return f"Could not retrieve stock price for {ticker.upper()}."
    except Exception as e:
        return f"Failed to retrieve stock price data: {e}"


tool = Tool(
    description="Get the current stock price for a given company ticker symbol.",
    function=get_stock_price,
    parameters=[
        Parameter(
            name="ticker",
            type="string",
            description="The stock ticker symbol, e.g., AAPL for Apple Inc.",
            required=True
        ),
        Parameter(
            name="currency",
            type="string",
            description="The currency format to display the stock price.",
            enum=["usd", "eur"],
            required=True
        ),
    ],
    metadata={
        "author": "Nathan Angstadt",
        "version": "1.0",
        "category": "Stocks",
    }
)
