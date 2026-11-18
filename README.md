# getWeather LangGraph Agent

A Python weather agent built with LangGraph and OpenAI. It geocodes locations and retrieves current and daily weather from Open-Meteo; no weather API key is required.

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
Copy-Item .env.example .env
```

Set `OPENAI_API_KEY` in `.env`, then run:

```powershell
python -m get_weather.cli "What is the weather in Seattle?"
```

Or install and use the console command:

```powershell
get-weather "Will it rain in Tokyo tomorrow?"
```

## Test

```powershell
python -m pip install -e ".[dev]"
pytest -q
```