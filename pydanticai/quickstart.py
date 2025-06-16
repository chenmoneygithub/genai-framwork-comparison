import asyncio
import getpass
import os
from dataclasses import dataclass
from datetime import date

from pydantic_ai import Agent
from pydantic_ai.tools import RunContext

if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key: ")


@dataclass
class WeatherService:
    async def get_forecast(self, location: str, forecast_date: date) -> str:
        # In real code: call weather API, DB queries, etc.
        return f"The forecast in {location} on {forecast_date} is 24°C and sunny."

    async def get_historic_weather(self, location: str, forecast_date: date) -> str:
        # In real code: call a historical weather API or DB
        return f"The weather in {location} on {forecast_date} was 18°C and partly cloudy."


weather_agent = Agent[WeatherService, str](
    "openai:gpt-4o-mini",
    deps_type=WeatherService,
    output_type=str,
    system_prompt="Providing a weather forecast at the locations the user provides.",
)


@weather_agent.tool
async def weather_forecast(
    ctx: RunContext[WeatherService],
    location: str,
    forecast_date: date,
) -> str:
    if forecast_date >= date.today():
        return await ctx.deps.get_forecast(location, forecast_date)
    else:
        return await ctx.deps.get_historic_weather(location, forecast_date)


async def main():
    return await weather_agent.run(
        "What will the weather be like in Paris on Tuesday?",
        deps=WeatherService(),
    )


if __name__ == "__main__":
    output = asyncio.run(main())
    print(output)
