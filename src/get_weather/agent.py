from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .weather import get_weather

SYSTEM_PROMPT = (
    "You are a concise weather assistant. Use the get_weather tool for every "
    "weather question. Ask for a location if it is missing, and report the "
    "location returned by the tool. Do not invent forecasts or observations."
)


def create_weather_agent():
    """Create an OpenAI-powered LangGraph weather agent."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return create_react_agent(model=model, tools=[get_weather], prompt=SYSTEM_PROMPT)
