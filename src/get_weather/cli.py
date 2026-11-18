from __future__ import annotations

import sys

from .agent import create_weather_agent


def main() -> None:
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Weather question: ").strip()

    if not question:
        raise SystemExit("Please enter a weather question.")

    agent = create_weather_agent()
    result = agent.invoke({"messages": [("user", question)]})
    messages = result["messages"]
    print(messages[-1].content)


if __name__ == "__main__":
    main()
