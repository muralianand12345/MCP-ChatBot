import os
import requests
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field


mcp = FastMCP(
    "Fetch Weather of a City",
    instructions="Fetch the weather of a city.",
    debug=False,
    log_level="INFO",
    host="0.0.0.0",
    port=8001,
)

API_KEY = os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise ValueError(
        "Please set the WEATHER_API_KEY environment variable with your WeatherAPI key."
    )


class ResponseFetchWeather(BaseModel):
    city: str = Field(..., description="City name")
    temperature: float = Field(..., description="Temperature in Celsius")
    description: str = Field(..., description="Weather description")


@mcp.tool()
def fetch_weather(city: str) -> ResponseFetchWeather:
    """Fetch weather information for a given city."""

    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

    response = requests.get(url)
    if response.status_code != 200:
        error_data = (
            response.json()
            if response.text
            else {"error": {"message": "Unknown error"}}
        )
        error_msg = error_data.get("error", {}).get("message", "Unknown error")
        raise Exception(f"Weather API error: {error_msg}")

    data = response.json()
    temperature = data["current"]["temp_c"]
    description = data["current"]["condition"]["text"]

    return ResponseFetchWeather(
        city=city,
        temperature=temperature,
        description=description,
    )


if __name__ == "__main__":
    mcp.run(transport="sse")
