from __future__ import annotations

import httpx
from langchain_core.tools import tool

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


@tool
def get_weather(location: str) -> str:
    """Get the current weather and today's forecast for a named city or place."""
    if not location.strip():
        return "Please provide a location name."

    with httpx.Client(timeout=15.0) as client:
        geocoding = client.get(GEOCODING_URL, params={"name": location, "count": 1})
        geocoding.raise_for_status()
        places = geocoding.json().get("results") or []
        if not places:
            return f"I could not find a location named '{location}'."

        place = places[0]
        latitude = place["latitude"]
        longitude = place["longitude"]
        response = client.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "timezone": "auto",
                "forecast_days": 1,
            },
        )
        response.raise_for_status()
        data = response.json()

    name = place.get("name", location)
    region = place.get("admin1")
    country = place.get("country")
    place_label = ", ".join(value for value in (name, region, country) if value)

    current = data["current"]
    daily = data["daily"]
    return (
        f"Weather for {place_label}:\n"
        f"Current temperature: {current['temperature_2m']}°C "
        f"(feels like {current['apparent_temperature']}°C)\n"
        f"Humidity: {current['relative_humidity_2m']}%\n"
        f"Wind: {current['wind_speed_10m']} km/h\n"
        f"Weather code: {current['weather_code']}\n"
        f"Today's low/high: {daily['temperature_2m_min'][0]}°C / "
        f"{daily['temperature_2m_max'][0]}°C\n"
        f"Maximum precipitation probability: "
        f"{daily['precipitation_probability_max'][0]}%"
    )
